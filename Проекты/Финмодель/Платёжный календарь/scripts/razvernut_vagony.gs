/**
 * Автоматический разворот Вагонов из Заявок
 * Триггер: onEdit — при изменении колонки G (Вагонов план) в листе Заявки
 *
 * Логика:
 * - Поменял G с 0 → 10 → добавляет 10 пустых строк в Вагоны (A=№ заявки)
 * - Поменял G с 10 → 12 → добавляет ещё 2 строки
 * - Поменял G с 10 → 8 → удаляет 2 ПУСТЫЕ заготовки (с данными не трогает)
 * - Удалил цифру → ничего не удаляется (безопасность)
 *
 * Установка:
 * 1. В Google Sheets: Расширения → Apps Script
 * 2. Удалить всё что было, вставить этот код
 * 3. Сохранить (Ctrl+S), дать имя проекту (например "Платёжный календарь")
 * 4. При первом редактировании G Google попросит разрешения — согласиться
 * 5. Готово — триггер работает автоматически
 */

const SHEET_ZAYAVKI = 'Заявки';
const SHEET_VAGONY = 'Вагоны';
const COL_PLAN = 7;      // G = Вагонов план
const COL_ZAYAVKA_ID = 1; // A = № заявки

function onEdit(e) {
  if (!e || !e.range) return;
  const sh = e.range.getSheet();
  if (sh.getName() !== SHEET_ZAYAVKI) return;
  if (e.range.getColumn() !== COL_PLAN) return;
  if (e.range.getRow() < 2) return; // шапка

  const row = e.range.getRow();
  const planCell = sh.getRange(row, COL_PLAN).getValue();
  const zayavkaId = sh.getRange(row, COL_ZAYAVKA_ID).getValue();

  if (!zayavkaId) return; // нет номера заявки — ничего не делаем
  if (planCell === '' || planCell === null) return; // стёрли — не удаляем ничего

  const planNum = Number(planCell);
  if (!planNum || planNum < 0 || planNum > 500) return; // защита от мусора

  syncVagony(zayavkaId, planNum);
}

/**
 * Синхронизировать Вагоны с планом по данной заявке.
 * - Считает текущие строки с A=zayavkaId
 * - Пустые (B и C незаполнены) — заготовки
 * - Непустые — реальные вагоны с данными
 * - Если план > реальные+заготовки → добавить N пустых
 * - Если план < реальные+заготовки → удалить min(лишние, пустые) заготовок
 *   (реальные не трогаем — вручную, если нужно)
 */
function syncVagony(zayavkaId, planNum) {
  const ss = SpreadsheetApp.getActive();
  const vg = ss.getSheetByName(SHEET_VAGONY);
  if (!vg) return;

  const lastRow = vg.getLastRow();
  const rowsToDelete = [];
  let withData = 0;
  let empty = 0;

  if (lastRow > 1) {
    const data = vg.getRange(2, 1, lastRow - 1, 3).getValues(); // A,B,C
    for (let i = 0; i < data.length; i++) {
      const rowZ = data[i][0]; // № заявки
      const rowB = data[i][1]; // № вагона
      const rowC = data[i][2]; // Дата
      if (rowZ == zayavkaId) {
        if ((rowB === '' || rowB === null) && (rowC === '' || rowC === null)) {
          empty++;
          rowsToDelete.push(i + 2); // 1-based + шапка
        } else {
          withData++;
        }
      }
    }
  }

  const total = withData + empty;

  if (planNum > total) {
    // добавить (planNum - total) пустых строк
    const toAdd = planNum - total;
    const newRows = [];
    for (let i = 0; i < toAdd; i++) {
      newRows.push([zayavkaId]); // только A, B и C пустые
    }
    const startRow = vg.getLastRow() + 1;
    vg.getRange(startRow, 1, toAdd, 1).setValues(newRows);
  } else if (planNum < total) {
    // удалить (total - planNum) ПУСТЫХ строк (с конца, чтоб не сбивались индексы)
    const toRemove = Math.min(total - planNum, empty);
    const removeRows = rowsToDelete.slice(-toRemove).sort((a, b) => b - a);
    for (const r of removeRows) {
      vg.deleteRow(r);
    }
  }
  // если planNum === total — ничего не делаем
}

/**
 * Ручной прогон по всем заявкам (на случай backfill).
 * Запуск: в Apps Script выбрать функцию syncAll → Run
 */
function syncAll() {
  const ss = SpreadsheetApp.getActive();
  const z = ss.getSheetByName(SHEET_ZAYAVKI);
  const lastRow = z.getLastRow();
  if (lastRow < 2) return;
  const data = z.getRange(2, 1, lastRow - 1, COL_PLAN).getValues();
  for (const row of data) {
    const id = row[0];
    const plan = Number(row[COL_PLAN - 1]);
    if (id && plan > 0 && plan <= 500) {
      syncVagony(id, plan);
    }
  }
  SpreadsheetApp.getActive().toast('Готово: синхронизированы все заявки');
}
