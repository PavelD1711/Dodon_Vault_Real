---
notion-bases: true
schema:
  - id: тип
    name: Тип
    type: select
    visible: true
    width: 140
    options:
      - value: дашборд
      - value: человек
      - value: инструкция
      - value: раздел
  - id: раздел
    name: Раздел
    type: select
    visible: true
    width: 140
    options:
      - value: "[[Networking/README|Networking]]"
  - id: дата_создания
    name: Дата создания
    type: select
    visible: true
    width: 140
    options:
      - value: 2026-09-22
  - id: дата_обновления
    name: Дата обновления
    type: select
    visible: true
    width: 140
    options:
      - value: 2026-09-22
  - id: теги
    name: Теги
    type: multiselect
    visible: true
    width: 140
    options:
      - value: networking
      - value: дашборд
      - value: человек
      - value: инструкция
      - value: sop
      - value: стратегия
      - value: партнёр
      - value: база-контактов
      - value: граф-связей
  - id: имя
    name: Имя
    type: text
    visible: true
    width: 200
  - id: фамилия
    name: Фамилия
    type: text
    visible: true
    width: 200
  - id: отчество
    name: Отчество
    type: text
    visible: true
    width: 200
  - id: короткое_имя
    name: Короткое имя
    type: text
    visible: true
    width: 200
  - id: компания
    name: Компания
    type: text
    visible: true
    width: 200
  - id: должность
    name: Должность
    type: text
    visible: true
    width: 200
  - id: город
    name: Город
    type: text
    visible: true
    width: 200
  - id: страна
    name: Страна
    type: text
    visible: true
    width: 200
  - id: часовой_пояс
    name: Часовой пояс
    type: text
    visible: true
    width: 200
  - id: email
    name: Email
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
  - id: telefon
    name: Telefon
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
  - id: telegram
    name: Telegram
    type: text
    visible: true
    width: 200
  - id: whatsapp
    name: Whatsapp
    type: text
    visible: true
    width: 200
  - id: linkedin
    name: Linkedin
    type: text
    visible: true
    width: 200
  - id: twitter
    name: Twitter
    type: text
    visible: true
    width: 200
  - id: youtube
    name: Youtube
    type: text
    visible: true
    width: 200
  - id: другие_соцсети
    name: Другие соцсети
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
  - id: дата_знакомства
    name: Дата знакомства
    type: text
    visible: true
    width: 200
  - id: откуда_знаю
    name: Откуда знаю
    type: text
    visible: true
    width: 200
  - id: представил
    name: Представил
    type: select
    visible: true
    width: 140
    options:
      - value: "[[]]"
  - id: статус
    name: Статус
    type: text
    visible: true
    width: 200
  - id: уровень_доверия
    name: Уровень доверия
    type: number
    visible: true
    width: 140
  - id: роли
    name: Роли
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: партнёр
      - value: коллега
  - id: экспертиза
    name: Экспертиза
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: стратегия
      - value: продукт
      - value: TMS
      - value: процессы
  - id: дата_последнего_контакта
    name: Дата последнего контакта
    type: text
    visible: true
    width: 200
  - id: периодичность
    name: Периодичность
    type: text
    visible: true
    width: 200
  - id: следующий_контакт
    name: Следующий контакт
    type: text
    visible: true
    width: 200
  - id: формат_общения
    name: Формат общения
    type: text
    visible: true
    width: 200
  - id: что_даёт_мне
    name: Что даёт мне
    type: text
    visible: true
    width: 200
  - id: что_я_могу_дать
    name: Что я могу дать
    type: text
    visible: true
    width: 200
  - id: общие_темы
    name: Общие темы
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: стратегия группы
      - value: iTrain / CargoLogic
      - value: Continental Bridge
      - value: Алгоритм
      - value: ДК Инкомтранс
  - id: семья
    name: Семья
    type: text
    visible: true
    width: 200
  - id: день_рождения
    name: День рождения
    type: text
    visible: true
    width: 200
  - id: значимые_даты
    name: Значимые даты
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
  - id: знаком_через
    name: Знаком через
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: "[[]]"
  - id: знает_людей
    name: Знает людей
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: "[[Волку Олег]]"
      - value: "[[Волку Владимир]]"
      - value: "[[Ольга Нюкалова]]"
  - id: качество_связей
    name: Качество связей
    type: text
    visible: true
    width: 200
  - id: связанные_проекты
    name: Связанные проекты
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: "[[Инкомтранс]]"
      - value: "[[Continental Bridge]]"
      - value: "[[CargoLogic]]"
      - value: "[[Стратштаб]]"
  - id: связанные_люди
    name: Связанные люди
    type: multiselect
    visible: true
    width: 140
    options:
      - value: "null"
      - value: "[[Волку Олег]]"
      - value: "[[Волку Владимир]]"
      - value: "[[Ольга Нюкалова]]"
  - id: целевая_аудитория
    name: Целевая аудитория
    type: text
    visible: true
    width: 200
  - id: название
    name: Название
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
---

> [!tip] Notion Bases
> This file is a database. Open it to see the table view.
