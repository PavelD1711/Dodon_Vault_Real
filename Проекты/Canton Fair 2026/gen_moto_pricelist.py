#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── шрифты ──────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVu",     f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuB",    f"{FONT_DIR}/DejaVuSans-Bold.ttf"))

# ── цвета ───────────────────────────────────────────────────────────────────
BLUE_DARK   = colors.HexColor("#1A3A5C")
BLUE_LIGHT  = colors.HexColor("#2E75B6")
BLUE_HEADER = colors.HexColor("#BDD7EE")
GRAY_ROW    = colors.HexColor("#F2F2F2")
GRAY_BLOCK  = colors.HexColor("#EFEFEF")
BORDER_CLR  = colors.HexColor("#CCCCCC")
WHITE       = colors.white
BLACK       = colors.black

# ── путь вывода ──────────────────────────────────────────────────────────────
OUT_PATH = "/home/work/vaults/dodon/Проекты/Canton Fair 2026/Прайс-лист_Мототехника.pdf"

W, H = A4   # 595.28 x 841.89

def make_styles():
    s = getSampleStyleSheet()
    base = dict(fontName="DejaVu", leading=14)

    styles = {
        "title": ParagraphStyle("title",
            fontName="DejaVuB", fontSize=18, textColor=WHITE,
            alignment=TA_LEFT, leading=22, spaceAfter=0),
        "subtitle": ParagraphStyle("subtitle",
            fontName="DejaVu", fontSize=9, textColor=colors.HexColor("#DDDDDD"),
            alignment=TA_LEFT, leading=12, spaceAfter=0),
        "section_header": ParagraphStyle("section_header",
            fontName="DejaVuB", fontSize=13, textColor=WHITE,
            alignment=TA_LEFT, leading=17, spaceAfter=0),
        "body": ParagraphStyle("body", **base, fontSize=9,
            textColor=BLACK, spaceAfter=2),
        "body_bold": ParagraphStyle("body_bold",
            fontName="DejaVuB", fontSize=9, textColor=BLACK,
            leading=14, spaceAfter=2),
        "cell": ParagraphStyle("cell", **base, fontSize=8.5,
            textColor=BLACK),
        "cell_bold": ParagraphStyle("cell_bold",
            fontName="DejaVuB", fontSize=8.5, textColor=BLUE_DARK,
            leading=14),
        "contact_label": ParagraphStyle("contact_label",
            fontName="DejaVuB", fontSize=8, textColor=BLUE_DARK,
            leading=13),
        "contact_line": ParagraphStyle("contact_line",
            fontName="DejaVu", fontSize=8, textColor=BLACK,
            leading=13),
        "footer": ParagraphStyle("footer",
            fontName="DejaVu", fontSize=7.5, textColor=colors.HexColor("#888888"),
            alignment=TA_CENTER, leading=11),
        "page_num": ParagraphStyle("page_num",
            fontName="DejaVu", fontSize=7.5, textColor=colors.HexColor("#888888"),
            alignment=TA_RIGHT, leading=11),
        "note": ParagraphStyle("note",
            fontName="DejaVu", fontSize=7.5, textColor=colors.HexColor("#555555"),
            leading=11, spaceAfter=0),
    }
    return styles

ST = make_styles()

# ── позиции ─────────────────────────────────────────────────────────────────
POSITIONS = [
    {
        "title": "1. Самокат аккумуляторный (E-Scooter)",
        "rows": [
            ("Мощность мотора, Вт",         "___ Вт (номинал / пик)",      "", ""),
            ("Напряжение системы",           "36 / 48 / 60 В",             "", ""),
            ("Ёмкость АКБ",                  "___ Ач / ___ Вт·ч",          "", ""),
            ("Тип АКБ",                      "Li-ion / LiFePO4",           "", ""),
            ("Запас хода, км",               "___ км",                      "", ""),
            ("Макс. скорость, км/ч",         "___ км/ч",                    "", ""),
            ("Макс. нагрузка, кг",           "___ кг",                      "", ""),
            ("Диаметр колёс",                "8\" / 8.5\" / 10\"",          "", ""),
            ("Тип колёс",                    "пневматические / сплошные",   "", ""),
            ("Тормоза",                      "механические / эл. / диск.",  "", ""),
            ("Подвеска",                     "да / нет",                    "", ""),
            ("Складная конструкция",         "да / нет",                    "", ""),
            ("Дисплей",                      "да / нет",                    "", ""),
            ("Время зарядки, ч",             "___ ч",                       "", ""),
            ("Вес, кг",                      "___ кг",                      "", ""),
            ("Сертификаты",                  "CE / WVTA / CoC",             "", ""),
        ]
    },
    {
        "title": "2. Трицикл карго электрический",
        "rows": [
            ("Мощность мотора, Вт",         "___ Вт (номинал / пик)",      "", ""),
            ("Напряжение",                   "48 / 60 / 72 В",             "", ""),
            ("Ёмкость АКБ",                  "___ Ач / ___ Вт·ч",          "", ""),
            ("Тип АКБ",                      "Li-ion / LiFePO4 / Lead-acid","", ""),
            ("Запас хода, км",               "___ км",                      "", ""),
            ("Макс. скорость, км/ч",         "___ км/ч",                    "", ""),
            ("Грузоподъёмность, кг",         "___ кг",                      "", ""),
            ("Тип кузова",                   "платформа / фургон / контейнер","",""),
            ("Размер кузова, мм",            "___ × ___ × ___",             "", ""),
            ("Тормоза",                      "дисковые / барабанные",       "", ""),
            ("Время зарядки, ч",             "___ ч",                       "", ""),
            ("Вес, кг",                      "___ кг",                      "", ""),
            ("Сертификаты",                  "CE / EEC",                    "", ""),
        ]
    },
    {
        "title": "3. Квадроцикл ATV (150/200/250/300 cc)",
        "rows": [
            ("Объём двигателя, cc",          "150 / 200 / 250 / 300",       "", ""),
            ("Тип двигателя",                "4-такт / 2-такт",             "", ""),
            ("Охлаждение",                   "воздушное / водяное",         "", ""),
            ("Мощность, л.с./кВт",           "___ л.с. / ___ кВт",          "", ""),
            ("КПП",                          "автомат / полуавтомат / мех.", "", ""),
            ("Привод",                       "2WD / 4WD",                   "", ""),
            ("Блокировка дифференциала",     "да / нет",                    "", ""),
            ("Макс. нагрузка, кг",           "___ кг",                      "", ""),
            ("Объём бака, л",                "___ л",                       "", ""),
            ("Электростартер",               "да / нет",                    "", ""),
            ("Лебёдка",                      "да / нет",                    "", ""),
            ("Сертификаты",                  "CE / EPA / EEC",              "", ""),
        ]
    },
    {
        "title": "4. Мотоцикл (125/150/200/250/300 cc)",
        "rows": [
            ("Объём двигателя, cc",          "125 / 150 / 200 / 250 / 300", "", ""),
            ("Тип двигателя",                "4-такт / 2-такт",             "", ""),
            ("Охлаждение",                   "воздушное / водяное",         "", ""),
            ("Мощность, л.с.",               "___ л.с.",                     "", ""),
            ("Тип",                          "дорожный / эндуро / кросс / питбайк / чоппер","",""),
            ("КПП, ступеней",                "___",                         "", ""),
            ("Тормоза перед/зад",            "дисковые / барабанные",       "", ""),
            ("ABS",                          "да / нет",                    "", ""),
            ("Объём бака, л",                "___ л",                       "", ""),
            ("Электростартер",               "да / нет",                    "", ""),
            ("Освещение",                    "LED / галоген",               "", ""),
            ("Сертификаты",                  "CE / EEC / EPA",              "", ""),
        ]
    },
    {
        "title": "5. Мотоблок (7 л.с. / 10 л.с.)",
        "rows": [
            ("Мощность, л.с.",               "7 / 10",                      "", ""),
            ("Объём двигателя, см³",         "___ см³",                     "", ""),
            ("Тип двигателя",                "4-такт / дизель",             "", ""),
            ("Тип привода",                  "ременной / редукторный",      "", ""),
            ("Охлаждение",                   "воздушное / водяное",         "", ""),
            ("КПП",                          "___ вперёд / ___ назад",      "", ""),
            ("Ширина обработки, мм",         "___ мм",                      "", ""),
            ("Глубина обработки, мм",        "___ мм",                      "", ""),
            ("Объём бака, л",                "___ л",                       "", ""),
            ("Электростартер",               "да / нет",                    "", ""),
            ("Навесное",                     "плуг / окучник / картофелекопалка / тележка","",""),
            ("Вес, кг",                      "___ кг",                      "", ""),
        ]
    },
    {
        "title": "6. Минитрактор (12–25 л.с.)",
        "rows": [
            ("Мощность, л.с.",               "12 / 15 / 18 / 22 / 25",     "", ""),
            ("Объём двигателя, см³",         "___ см³",                     "", ""),
            ("Тип",                          "бензин / дизель",             "", ""),
            ("Охлаждение",                   "воздушное / водяное",         "", ""),
            ("КПП",                          "___ вперёд / ___ назад",      "", ""),
            ("Привод",                       "2WD / 4WD",                   "", ""),
            ("ВОМ",                          "да / нет, ___ об/мин",        "", ""),
            ("Гидравлика",                   "да / нет",                    "", ""),
            ("Грузоподъёмность навески, кг", "___ кг",                      "", ""),
            ("Навесное",                     "фреза / плуг / косилка / отвал / прицеп","",""),
            ("Объём бака, л",                "___ л",                       "", ""),
            ("Электростартер",               "да / нет",                    "", ""),
            ("Вес, кг",                      "___ кг",                      "", ""),
            ("Сертификаты",                  "CE / EPA",                    "", ""),
        ]
    },
]

CONTACT_FIELDS = [
    ("Производитель:",       "___________________________"),
    ("Контактное лицо:",     "_________________________"),
    ("WhatsApp / WeChat:",   "_______________________"),
    ("Email:",               "___________________________________"),
    ("Сайт / Alibaba:",      "__________________________"),
    ("Стенд / Зал:",         "____________________________"),
    ("Примечания:",          "_____________________________"),
]

COL_W_PCT  = [0.40, 0.25, 0.20, 0.15]   # Параметр / Спецификация / Цена FOB / MOQ

def build_header_table(title_text):
    """Синий блок-заголовок позиции."""
    available = W - 25*mm - 25*mm   # margins
    data = [[Paragraph(title_text, ST["section_header"])]]
    t = Table(data, colWidths=[available])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BLUE_DARK]),
    ]))
    return t

def build_param_table(rows):
    available = W - 25*mm - 25*mm
    cw = [available * p for p in COL_W_PCT]

    header_data = [
        Paragraph("Параметр",       ST["cell_bold"]),
        Paragraph("Спецификация",   ST["cell_bold"]),
        Paragraph("Цена FOB, USD",  ST["cell_bold"]),
        Paragraph("MOQ, шт.",       ST["cell_bold"]),
    ]

    table_data = [header_data]
    for i, (param, spec, price, moq) in enumerate(rows):
        table_data.append([
            Paragraph(param, ST["cell"]),
            Paragraph(spec,  ST["cell"]),
            Paragraph(price if price else "",  ST["cell"]),
            Paragraph(moq   if moq   else "",  ST["cell"]),
        ])

    style = TableStyle([
        # заголовок
        ("BACKGROUND",    (0, 0), (-1, 0),  BLUE_HEADER),
        ("FONTNAME",      (0, 0), (-1, 0),  "DejaVuB"),
        ("FONTSIZE",      (0, 0), (-1, 0),  8.5),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLUE_DARK),
        # чётные строки
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GRAY_ROW]),
        # общее
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        # линии цены и MOQ — подчёркнуты для заполнения
        ("LINEBELOW",     (2, 1), (3, -1),  0.8, colors.HexColor("#AAAAAA")),
    ])
    t = Table(table_data, colWidths=cw, repeatRows=1)
    t.setStyle(style)
    return t

def build_contact_block():
    available = W - 25*mm - 25*mm
    cw_label = available * 0.35
    cw_value = available * 0.65

    data = []
    for label, blank in CONTACT_FIELDS:
        data.append([
            Paragraph(label,  ST["contact_label"]),
            Paragraph(blank,  ST["contact_line"]),
        ])

    t = Table(data, colWidths=[cw_label, cw_value])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GRAY_BLOCK),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER_CLR),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW",     (1, 0), (1, -1),  0.7, colors.HexColor("#AAAAAA")),
    ]))
    return t


# ── колонтитулы ──────────────────────────────────────────────────────────────
def footer_cb(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVu", 7.5)
    canvas.setFillColor(colors.HexColor("#888888"))

    footer_text = "Canton Fair 2026  |  Meserias  |  Конфиденциально"
    page_text   = f"Стр. {doc.page}"

    y = 15*mm
    canvas.drawCentredString(W / 2, y, footer_text)
    canvas.drawRightString(W - 20*mm, y, page_text)

    # линия сверху колонтитула
    canvas.setStrokeColor(BORDER_CLR)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, y + 5*mm, W - 20*mm, y + 5*mm)

    canvas.restoreState()


# ── COVER страница ───────────────────────────────────────────────────────────
def build_cover():
    elements = []
    available = W - 25*mm - 25*mm

    # Синяя плашка-заголовок документа
    cover_data = [[
        Paragraph("ПРАЙС-ЛИСТ ПОСТАВЩИКА", ParagraphStyle(
            "cover_main", fontName="DejaVuB", fontSize=22,
            textColor=WHITE, leading=28, alignment=TA_LEFT)),
    ]]
    cover_sub_data = [[
        Paragraph(
            "Категория: Мототехника\nCanton Fair 2026  |  Гуанчжоу, Китай\nMeserias — конфиденциально",
            ParagraphStyle("cover_sub", fontName="DejaVu", fontSize=11,
                textColor=colors.HexColor("#CCDDEE"), leading=16, alignment=TA_LEFT))
    ]]

    for d, bg in [(cover_data, BLUE_DARK), (cover_sub_data, BLUE_LIGHT)]:
        t = Table(d, colWidths=[available])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("TOPPADDING",    (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
            ("LEFTPADDING",   (0, 0), (-1, -1), 14),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ]))
        elements.append(t)

    elements.append(Spacer(1, 10*mm))

    # Содержание
    toc_rows = [
        [Paragraph("№", ST["cell_bold"]),
         Paragraph("Наименование позиции", ST["cell_bold"]),
         Paragraph("Страниц.", ST["cell_bold"])],
    ]
    for i, pos in enumerate(POSITIONS, 1):
        toc_rows.append([
            Paragraph(str(i), ST["cell"]),
            Paragraph(pos["title"][3:], ST["cell"]),   # убираем "N. "
            Paragraph("", ST["cell"]),
        ])

    toc = Table(toc_rows, colWidths=[available*0.07, available*0.78, available*0.15])
    toc.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), BLUE_HEADER),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GRAY_ROW]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("FONTNAME",      (0, 0), (-1, 0), "DejaVuB"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",     (0, 0), (-1, 0), BLUE_DARK),
    ]))
    elements.append(Paragraph("Содержание", ParagraphStyle(
        "toc_hdr", fontName="DejaVuB", fontSize=12,
        textColor=BLUE_DARK, leading=16, spaceAfter=5)))
    elements.append(toc)

    elements.append(Spacer(1, 8*mm))

    # Инструкция
    instr = (
        "<b>Инструкция по заполнению:</b><br/>"
        "1. Впишите данные поставщика в каждый блок контактов.<br/>"
        "2. В колонке «Цена FOB, USD» укажите цену на единицу товара (FOB Shanghai или другой порт).<br/>"
        "3. В колонке «MOQ, шт.» укажите минимальный объём заказа.<br/>"
        "4. Выделите / обведите выбранные варианты в колонке «Спецификация».<br/>"
        "5. Сохраните заполненный лист или сфотографируйте — отправьте в чат."
    )
    elements.append(Paragraph(instr, ParagraphStyle(
        "instr", fontName="DejaVu", fontSize=9, textColor=BLACK,
        leading=14, spaceAfter=0,
        borderColor=BORDER_CLR, borderWidth=0.5, borderPadding=8,
        backColor=GRAY_BLOCK)))

    return elements


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=22*mm, bottomMargin=24*mm,
        title="Прайс-лист Мототехника — Canton Fair 2026",
        author="Meserias / Pablo",
        subject="Canton Fair 2026 Supplier Price List",
    )

    story = []

    # — обложка —
    story.extend(build_cover())

    # — позиции —
    for pos in POSITIONS:
        story.append(Spacer(1, 8*mm))
        story.append(build_header_table(pos["title"]))
        story.append(Spacer(1, 2*mm))
        story.append(build_param_table(pos["rows"]))
        story.append(Spacer(1, 3*mm))

        # заголовок контактного блока
        available = W - 25*mm - 25*mm
        contact_hdr_data = [[Paragraph("📋 Контакты производителя", ParagraphStyle(
            "ch", fontName="DejaVuB", fontSize=9, textColor=BLUE_DARK,
            leading=13, alignment=TA_LEFT))]]
        ch = Table(contact_hdr_data, colWidths=[available])
        ch.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), BLUE_HEADER),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(ch)
        story.append(build_contact_block())

    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)
    print(f"✅ PDF создан: {OUT_PATH}")

if __name__ == "__main__":
    main()
