---
notion-bases: true
schema:
  - id: database-plugin
    name: Database-plugin
    type: text
    visible: true
    width: 200
  - id: name
    name: Name
    type: text
    visible: true
    width: 200
  - id: role
    name: Role
    type: select
    visible: true
    width: 140
    options:
      - value: Менеджер по продажам
      - value: Бизнес-ассистент Генерального директора
      - value: Клиентский менеджер
      - value: Техобслуживание
      - value: Руководитель экспедирования
      - value: Диспетчер
  - id: start_date
    name: Start date
    type: date
    visible: true
    width: 140
  - id: end_date
    name: End date
    type: date
    visible: true
    width: 140
  - id: status
    name: Status
    type: select
    visible: true
    width: 140
    options:
      - value: fired
      - value: probation
      - value: active
  - id: manager
    name: Manager
    type: select
    visible: true
    width: 140
    options:
      - value: Додон Павел
  - id: format
    name: Format
    type: select
    visible: true
    width: 140
    options:
      - value: офис
  - id: tags
    name: Tags
    type: multiselect
    visible: true
    width: 140
    options:
      - value: сотрудник
views:
  - id: default
    type: table
    filters: []
    sorts:
      - columnId: database-plugin
        direction: desc
      - columnId: status
        direction: desc
      - columnId: name
        direction: asc
    hiddenColumns: []
    columnWidths: {}
    pinnedColumnId: database-plugin
    rowHeight: compact
    activePills:
      - id: 363e6daa-36f8-4330-95fa-229317f81c79
        columnId: status
        operator: is
        value: ""
        conjunction: and
    columnOrder:
      - role
      - database-plugin
      - name
      - start_date
      - end_date
      - status
      - manager
      - format
      - tags
    wrapText: false
  - id: 3c16c3d5-73ea-40af-9cba-cb91757d0795
    type: timeline
    filters: []
    sorts: []
    hiddenColumns: []
    columnWidths: {}
    pinnedColumnId:
    name: Timeline
  - id: f5498af2-2c1b-4239-8a01-2e547d68bfa0
    type: board
    filters: []
    sorts: []
    hiddenColumns: []
    columnWidths: {}
    pinnedColumnId:
    name: Board
---

> [!tip] Notion Bases
> This file is a database. Open it to see the table view.
