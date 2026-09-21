#!/usr/bin/env python3
"""
build_bdr.py — построение БДР и БДДС группы из файла «Интеркомпани» xlsx (1С-выгрузка).

Usage:
    python3 build_bdr.py <input.xlsx> <period_label> [--usd-rate 85]

Output:
    stdout — форматированный БДР + БДДС + «выпадающая выручка на СП»
    <period_label>_bdr.json — машиночитаемо
"""

import sys
import json
import zipfile
import shutil
import tempfile
import os
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. Загрузка xlsx (с фиксом sharedStrings.xml case)
# ============================================================

def load_xlsx_safe(path):
    """1С-выгрузка иногда содержит SharedStrings.xml с заглавной S — openpyxl падает.
    Перепаковываем во временный файл с правильным именем."""
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    tmp.close()
    try:
        with zipfile.ZipFile(path, 'r') as zin, zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.namelist():
                data = zin.read(item)
                new_name = 'xl/sharedStrings.xml' if item == 'xl/SharedStrings.xml' else item
                zout.writestr(new_name, data)
        return pd.read_excel(tmp.name, sheet_name=0, header=None)
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass


# ============================================================
# 2. Схема столбцов «Интеркомпани»
# ============================================================

COLS = {
    'wagon': 0, 'date': 2, 'from': 4, 'to': 7, 'client': 8,
    'sale1_org': 9,  'sale1_cur': 10, 'sale1_amt': 11, 'sale1_vat': 12,
    'sale3_org': 13, 'sale3_cur': 14, 'sale3_amt': 15, 'sale3_vat': 16,
}

# Затратные блоки: (col_org, col_exec, col_amt, col_vat, статья_БДР, бддс_группа)
COST_BLOCKS = [
    (17, 18, 19, 20, 'Предоставление вагона',    'Аренда вагонов'),
    (21, 22, 23, 24, 'Тариф РФ',                  'Оплата РЖД'),
    (25, 26, 27, 28, 'Транзит КЗХ',               'Оплата КЗХ'),
    (29, 30, 31, 32, 'Бонус заказчик',            'Бонусы клиентам'),  # -Выручка
    (33, 34, 35, 36, 'Подача-уборка',             'Прочие прямые'),
    (37, 38, 39, 40, 'Подача-уборка',             'Прочие прямые'),
    (41, 42, 43, 44, 'ЗПУ',                       'Прочие прямые'),
    (45, 46, 47, 48, 'Маневровая',                'Прочие прямые'),
    (49, 50, 51, 52, 'Тариф порожний',            'Оплата РЖД'),
    (53, 54, 55, 56, 'Тариф СНГ',                 'Прочие прямые'),
    (57, 58, 59, 60, 'Погрузка',                  'Прочие прямые'),
    (61, 62, 63, 64, 'Этран',                     'Прочие прямые'),
    (65, 66, 67, 68, 'Штраф',                     'Прочие прямые'),
]

GROUP_JULS = ['Транзит', 'Северный Путь', 'ИНКОМ ТРАНС ООО']
JUL_SHORT = {'Транзит': 'Транзит', 'Северный Путь': 'СП', 'ИНКОМ ТРАНС ООО': 'ИТ'}


# ============================================================
# 3. Нормализация значений (НДС + валюта)
# ============================================================

def netto_from_gross(gross, vat_str):
    """Приводим значение к сумме без НДС."""
    if pd.isna(gross) or gross == 0:
        return 0.0
    try:
        gross = float(gross)
    except (ValueError, TypeError):
        return 0.0
    if pd.isna(vat_str):
        return gross
    s = str(vat_str).strip()
    if s in ('Без НДС', '0%', '0', 'НДС не облагается'):
        return gross
    if s == '22%':
        return gross / 1.22
    if s == '20%':
        return gross / 1.20
    if s == '10%':
        return gross / 1.10
    # Неизвестная ставка — возвращаем как есть
    return gross


def to_rub(amt, cur, usd_rate):
    """Пересчитываем в RUB."""
    if pd.isna(amt) or amt == 0:
        return 0.0
    if pd.isna(cur):
        return float(amt)
    cur = str(cur).upper().strip()
    if cur == 'USD':
        return float(amt) * usd_rate
    return float(amt)


# ============================================================
# 4. Ядро: разложение по ЮЛ
# ============================================================

def build_by_jul(data, usd_rate):
    """
    Возвращает:
    {
        'revenue': {jul: {статья: сумма_RUB}},
        'costs':   {jul: {статья: сумма_RUB}},
    }
    """
    result = {
        'revenue': {jul: {} for jul in GROUP_JULS + ['Прочие']},
        'costs':   {jul: {} for jul in GROUP_JULS + ['Прочие']},
    }

    def add(bucket, jul, item, amt):
        if jul not in result[bucket]:
            result[bucket][jul] = {}
        result[bucket][jul][item] = result[bucket][jul].get(item, 0.0) + amt

    for _, row in data.iterrows():
        # Продажа 1
        s1_org = row.get(COLS['sale1_org'])
        s1_amt = netto_from_gross(row.get(COLS['sale1_amt']), row.get(COLS['sale1_vat']))
        s1_rub = to_rub(s1_amt, row.get(COLS['sale1_cur']), usd_rate)
        if s1_rub > 0 and pd.notna(s1_org):
            jul = s1_org if s1_org in GROUP_JULS else 'Прочие'
            add('revenue', jul, 'Продажа 1 (осн.)', s1_rub)

        # Продажа 3
        s3_org = row.get(COLS['sale3_org'])
        s3_amt = netto_from_gross(row.get(COLS['sale3_amt']), row.get(COLS['sale3_vat']))
        s3_rub = to_rub(s3_amt, row.get(COLS['sale3_cur']), usd_rate)
        if s3_rub > 0 and pd.notna(s3_org):
            jul = s3_org if s3_org in GROUP_JULS else 'Прочие'
            add('revenue', jul, 'Продажа 3 (доп.)', s3_rub)

        # Затраты (13 блоков)
        for col_org, col_exec, col_amt, col_vat, item, _ in COST_BLOCKS:
            org = row.get(col_org)
            amt = netto_from_gross(row.get(col_amt), row.get(col_vat))
            if amt > 0 and pd.notna(org):
                jul = org if org in GROUP_JULS else 'Прочие'
                # Бонус — это отрицательная выручка (комиссия клиенту)
                if item == 'Бонус заказчик':
                    add('revenue', jul, 'Бонусы (−)', -amt)
                else:
                    add('costs', jul, item, amt)

    return result


# ============================================================
# 5. Расчёт «выпадающей выручки на СП» (метод A)
# ============================================================

def fallen_revenue_sp(data, usd_rate):
    """
    Для каждого рейса:
        costs_СП    = сумма затрат, где org = СП
        revenue_СП  = Продажа 1 + Продажа 3, где org = СП
        revenue_oth = Продажа 1 + Продажа 3, где org ≠ СП (Транзит / ИТ / пусто)
    Если costs_СП > 0 и revenue_oth > 0 → выпадающая = revenue_oth
    """
    total = 0.0
    by_client = {}
    by_receiver = {'Транзит': 0.0, 'ИНКОМ ТРАНС ООО': 0.0, 'Прочие': 0.0}

    for _, row in data.iterrows():
        # Затраты СП
        costs_sp = 0.0
        for col_org, _, col_amt, col_vat, _, _ in COST_BLOCKS:
            if row.get(col_org) == 'Северный Путь':
                costs_sp += netto_from_gross(row.get(col_amt), row.get(col_vat))
        if costs_sp <= 0:
            continue

        # Выручка не-СП
        revenue_oth = 0.0
        breakdown = {}
        for sale_org, sale_amt, sale_cur, sale_vat, label in [
            (COLS['sale1_org'], COLS['sale1_amt'], COLS['sale1_cur'], COLS['sale1_vat'], 'Продажа 1'),
            (COLS['sale3_org'], COLS['sale3_amt'], COLS['sale3_cur'], COLS['sale3_vat'], 'Продажа 3'),
        ]:
            org = row.get(sale_org)
            if pd.notna(org) and org != 'Северный Путь':
                amt = netto_from_gross(row.get(sale_amt), row.get(sale_vat))
                rub = to_rub(amt, row.get(sale_cur), usd_rate)
                revenue_oth += rub
                if rub > 0:
                    receiver = org if org in ('Транзит', 'ИНКОМ ТРАНС ООО') else 'Прочие'
                    by_receiver[receiver] += rub
                    breakdown[label] = rub

        if revenue_oth > 0:
            total += revenue_oth
            client = row.get(COLS['client'])
            if pd.notna(client):
                by_client[client] = by_client.get(client, 0.0) + revenue_oth

    return {
        'total_rub': total,
        'by_client': dict(sorted(by_client.items(), key=lambda x: -x[1])[:15]),
        'by_receiver': by_receiver,
    }


# ============================================================
# 6. Форматирование вывода
# ============================================================

WIDTH = 14

def fmt(x):
    """Форматирование числа под столбец фиксированной ширины."""
    if abs(x) < 1:
        return f'{"—":>{WIDTH}}'
    return f'{x:>{WIDTH},.0f}'.replace(',', ' ')


def print_bdr(result, period, revenue_articles, cost_articles):
    total_width = 30 + WIDTH * 4
    print()
    print('═' * total_width)
    print(f'  БДР {period} — КОНСОЛИДИРОВАННЫЙ (в тыс. RUB, нетто без НДС)')
    print('═' * total_width)

    cols = ['Транзит', 'Северный Путь', 'ИНКОМ ТРАНС ООО']
    header = ' ' * 30 + ''.join(f'{JUL_SHORT[c]:>{WIDTH}}' for c in cols) + f'{"Итого":>{WIDTH}}'
    print(header)
    print('─' * total_width)

    print('ВЫРУЧКА')
    total_rev = {c: 0.0 for c in cols + ['Итого']}
    for art in revenue_articles:
        row = f'  {art:<28}'
        total = 0.0
        for c in cols:
            v = result['revenue'][c].get(art, 0.0) / 1000
            row += fmt(v)
            total_rev[c] += v
            total += v
        row += fmt(total)
        total_rev['Итого'] += total
        print(row)
    print('─' * total_width)
    row = f'  {"Итого выручка":<28}'
    for c in cols:
        row += fmt(total_rev[c])
    row += fmt(total_rev['Итого'])
    print(row)

    print()
    print('ПРЯМЫЕ ЗАТРАТЫ')
    total_cost = {c: 0.0 for c in cols + ['Итого']}
    for art in cost_articles:
        row = f'  {art:<28}'
        total = 0.0
        for c in cols:
            v = result['costs'][c].get(art, 0.0) / 1000
            row += fmt(v)
            total_cost[c] += v
            total += v
        row += fmt(total)
        total_cost['Итого'] += total
        print(row)
    print('─' * total_width)
    row = f'  {"Итого затрат":<28}'
    for c in cols:
        row += fmt(total_cost[c])
    row += fmt(total_cost['Итого'])
    print(row)

    print()
    row = f'  {"ВАЛОВАЯ ПРИБЫЛЬ":<28}'
    margin_data = {}
    for c in cols + ['Итого']:
        vp = total_rev[c] - total_cost[c]
        margin_data[c] = vp
        row += fmt(vp)
    print(row)

    row = f'  {"Маржа, %":<28}'
    for c in cols + ['Итого']:
        rev = total_rev[c]
        pct = margin_data[c] / rev * 100 if rev > 0 else 0
        row += f'{pct:>{WIDTH-1}.1f}%'
    print(row)
    print('═' * total_width)


def print_fallen(fallen, period):
    print()
    print('═' * 88)
    print(f'  ВЫПАДАЮЩАЯ ВЫРУЧКА НА СП {period} (метод A, точный)')
    print('═' * 88)
    print(f'  Итого:  {fallen["total_rub"] / 1_000_000:.2f} млн RUB')
    print()
    print('  По получателям (кому клиент заплатил вместо СП):')
    for receiver, amt in fallen['by_receiver'].items():
        if amt > 0:
            print(f'    {receiver:<25}{amt / 1_000_000:>8.2f} млн RUB')
    print()
    print('  ТОП-10 клиентов по «выпадающей»:')
    for client, amt in list(fallen['by_client'].items())[:10]:
        print(f'    {client[:35]:<38}{amt / 1_000_000:>8.2f} млн RUB')
    print('═' * 88)


# ============================================================
# 7. Main
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("Usage: build_bdr.py <input.xlsx> <period_label> [--usd-rate 85]")
        sys.exit(1)

    path = sys.argv[1]
    period = sys.argv[2]
    usd_rate = 85.0
    if '--usd-rate' in sys.argv:
        idx = sys.argv.index('--usd-rate')
        usd_rate = float(sys.argv[idx + 1])

    print(f'\n[info] Загружаю {path}, курс USD = {usd_rate} ₽')
    df = load_xlsx_safe(path)
    data = df.iloc[7:].reset_index(drop=True)
    data = data[data[COLS['date']].notna()]
    print(f'[info] Рейсов: {len(data)}, вагонов: {data[COLS["wagon"]].nunique()}')

    result = build_by_jul(data, usd_rate)

    # Собираем список статей (без дубликатов, в порядке появления)
    revenue_articles = ['Продажа 1 (осн.)', 'Продажа 3 (доп.)', 'Бонусы (−)']
    cost_articles = []
    for _, _, _, _, item, _ in COST_BLOCKS:
        if item != 'Бонус заказчик' and item not in cost_articles:
            cost_articles.append(item)

    print_bdr(result, period, revenue_articles, cost_articles)

    fallen = fallen_revenue_sp(data, usd_rate)
    print_fallen(fallen, period)

    # Сохраняем машиночитаемо
    out_json = Path(path).parent / f'{period}_bdr.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump({
            'period': period,
            'usd_rate': usd_rate,
            'trips': len(data),
            'wagons_unique': int(data[COLS['wagon']].nunique()),
            'result': result,
            'fallen_revenue_sp': fallen,
        }, f, ensure_ascii=False, indent=2, default=float)
    print(f'\n[ok] JSON сохранён: {out_json}')


if __name__ == '__main__':
    main()
