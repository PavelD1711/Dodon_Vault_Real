---
notion-bases: true
schema:
  - id: тип
    name: Тип
    type: select
    visible: true
    width: 140
    options:
      - value: идея
      - value: дашборд
      - value: мета
  - id: статус
    name: Статус
    type: select
    visible: true
    width: 140
    options:
      - value: не_обработана
  - id: важность
    name: Важность
    type: text
    visible: true
    width: 200
  - id: контекст
    name: Контекст
    type: select
    visible: true
    width: 140
    options:
      - value: бизнес
  - id: источник
    name: Источник
    type: text
    visible: true
    width: 200
  - id: дата_получения
    name: Дата получения
    type: text
    visible: true
    width: 200
  - id: результат
    name: Результат
    type: select
    visible: true
    width: 140
    options:
      - value: "[[]]"
  - id: tags
    name: Tags
    type: multiselect
    visible: true
    width: 140
    options:
      - value: идея
      - value: входящие
      - value: аналитика
  - id: проект_контекст
    name: Проект контекст
    type: text
    visible: true
    width: 200
views:
  - id: default
    type: table
    filters: []
    sorts: []
    hiddenColumns: []
    columnWidths: {}
  - id: e9ebea87-1cf4-46a6-adfc-aa24cc9d9043
    type: table
    filters: []
    sorts: []
    hiddenColumns: []
    columnWidths: {}
    pinnedColumnId:
    name: Table
    rowHeight: compact
    wrapText: false
---

> [!tip] Notion Bases
> This file is a database. Open it to see the table view.
