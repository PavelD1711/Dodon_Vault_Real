---
type: project
project_code: "CargoLogic"
title: "CargoLogic / iTrain — TMS-платформа для грузоотправителей"
status: active
owner: "[[Павел]]"
executors:
  - "[[Павел]]"
  - "[[Сергей Чирва]]"
  - "[[Pablo]]"
telegram_group: "-5180864406"
telegram_group_name: "CargoLogic"
mode: active
created: 2026-09-07
updated: 2026-09-07
related_docs:
  - "Google Doc v4 ФИНАЛ (13 разделов): https://docs.google.com/document/d/1MNoHiLmXMY8UrZrmz88kLeP1xEPT-IMekdpuk2qjGls/edit"
---

# Проект CargoLogic / iTrain

> **👋 Pablo, если ты открыл этот файл в сессии группы CargoLogic (`-5180864406`) в первый раз:**
> 1. `memory_search "CargoLogic репозиторий"` — доступ, ключи, история
> 2. Ключевые файлы памяти: `memory/2026-09-07.md`, `memory/2026-09-03.md`, `memory/2026-08-18.md`, `memory/2026-08-13.md`, `memory/2026-04-07.md`
> 3. **Репо клонирован:** `/home/work/.openclaw/workspace/projects/cargologic/CargoLogic/` — SSH-ключ Pablo привязан локально (`core.sshCommand`), `git pull` работает без флагов
> 4. **Перед работой с vault:** `cd /home/work/.openclaw/workspace/vaults/dodon && git pull` — другая сессия Pablo могла уже коммитнуть
> 5. **Перед работой с репо:** `cd projects/cargologic/CargoLogic && git pull` — Дмитрий коммитит каждый день

## О группе Telegram

- **ID:** `-5180864406`
- **Название:** CargoLogic
- **Участники:** Павел + Сергей Чирва + Pablo
- **Тема:** разработка TMS-платформы для грузоотправителей (не операторов) на пространстве 1520

## Режим Pablo в группе

**Активный режим:**
- Pablo активно ведёт проект по бизнес-модели и планированию разработки
- Отвечает на любые сообщения по теме
- Помогает Павлу и Сергею структурировать решения
- Ставит уточняющие вопросы когда данных для движения не хватает

## Границы контекста группы

**Что обсуждаем в группе:**
- Бизнес-модель CargoLogic (портрет клиента, ценностное предложение, ARR, ценообразование, каналы)
- Планирование и организация работы по разработке MVP
- Планирование и организация работы по боевым проектам (пилоты, внедрения)
- Конкурентный анализ (Trucker.ru Rail Cargo и др.)
- Roadmap продукта: этапы, вехи, ресурсы
- Взаимодействие с командой разработки, партнёрами, ранними клиентами
- Финмодель / юнит-экономика продукта

**Что НЕ обсуждаем в группе (уходит в другие каналы):**
- Стратегия Инкомтранса (оперирование парком) → личка Павла или Стратегический штаб
- Continental Bridge → своя группа
- Мессериаш → своя группа
- Личные мысли Павла → Рефлексия
- Найм / адаптация сотрудников → своя рабочая площадка

## Репозиторий GitHub (⚡ обновляем)

- **URL:** https://github.com/kuznetsov-kdv/CargoLogic
- **Локальный клон Pablo:** `/home/work/.openclaw/workspace/projects/cargologic/CargoLogic/`
- **Способ доступа:** SSH-ключ `~/.ssh/github_dodon_vault` (аккаунт `PavelD1711`, принят в collaborators 07.09.2026)
- **Ветки:** `main` (активная), `codex/support-interface`
- **Команда для pull:** `cd /home/work/.openclaw/workspace/projects/cargologic/CargoLogic && git pull` (SSH-команда привязана через `core.sshCommand`)
- **Активность:** 691 коммит за последние 30 дней (Кузнецов)
- **Стек:** .NET / C# (`CargoLogic.CentralServer`, `CargoLogic.Cli`, `CargoLogic.Domain`, `CargoLogic.Persistence.PostgreSql`)
- **Модели:** 13 YAML в `models/cargologic/` (core, planning, analytics, integration, modularity, configuration, platform-operations, shared-platform, distance-data, calculation-data, etran, etran-stub, reference-data)
- **Спеки:** ~80 markdown-файлов в `docs/superpowers/specs/`

## Ссылки на артефакты

- **Google Doc v4 ФИНАЛ бизнес-модели (13 разделов):** https://docs.google.com/document/d/1MNoHiLmXMY8UrZrmz88kLeP1xEPT-IMekdpuk2qjGls/edit
  Содержит: портрет клиента, 11-шаговый цикл, ядро (временные метки + атрибуция + док-база), 3 варианта бизнес-модели (ARR 60-250 млн ₽), конкуренты, пересмотр сроков
- **Оценка проекта в терминах Антара (03.09.2026):** 57-78 ЕР, 1000-1400 ч, 4,0-7,0 млн ₽ (см. `memory/2026-09-03.md`)
- **Обзор Trucker.ru Rail Cargo:** `memory/2026-04-07.md` (референс конкурента)
- **Устаревшие версии Google Doc:**
  - v1: https://docs.google.com/document/d/1Q4osrd_Q5NTV5ypbtfYDVIP554r_c9TUNSbZJlCMR1c/edit
  - v2: https://docs.google.com/document/d/1Of-lZpn_kqi67Wv4WCeMqKiNdVaoChPxoTI3bJ0CiQg/edit
  - v3: https://docs.google.com/document/d/1FbYCe9gXpriGcDjny_NhnC7zfr6LC_PzFZaye9qjPcM/edit

## Люди

### Павел Додон
- Владелец продукта, стратегия, ключевые решения

### Сергей Чирва
- Со-руководитель проекта
- Также участник **«Стратегический штаб / Нюкалова»** (`-5076995734`, см. TOOLS.md)
- Опыт: стратегический слой, отношения, работа с командой

### Pablo
- Ведение проектной документации, бизнес-модели, планирования, аналитики

## Открытые вопросы для запуска работы

- [ ] Утвердить финальный вариант бизнес-модели (из 3 в Google Doc v4)
- [ ] Согласовать целевую ARR (60 / 120 / 250 млн ₽)
- [ ] Утвердить состав MVP (какие из 13 компонентов)
- [ ] Определить сроки MVP (жёлтый / зелёный / критический сценарий)
- [ ] Кто разработчик — Антар или другие
- [ ] Первые пилотные клиенты — из клиентской базы Инкомтранса или новые

## План работы (черновой)

1. **Этап 1 — Бизнес-модель финализирована** (совместно с Сергеем)
   - Один вариант из 3 → защищённая гипотеза
   - Юнит-экономика посчитана
   - Конкурентное позиционирование зафиксировано

2. **Этап 2 — Roadmap MVP**
   - Состав MVP (что входит / что не входит)
   - Оценка ресурсов и сроков
   - Выбор подрядчика

3. **Этап 3 — Пилотные клиенты**
   - Список 3-5 первых клиентов
   - Условия пилота (стоимость / бесплатно / доля)
   - Метрики успеха пилота

4. **Этап 4 — Запуск разработки MVP**
   - Контракт с подрядчиком
   - Календарь релизов
   - Регулярные апдейты в группу

## История

- **2026-09-07 (12:52)** — создан README проекта CargoLogic после получения chat_id группы от Павла (`-5180864406`). Первоначально Pablo ошибочно связал этот chat_id с проектом «Бизнес-ассистент» — исправлено уточнением Павла в голосовом.
- **2026-09-07 (16:39)** — Павел добавил аккаунт `PavelD1711` (с ключом Pablo) в collaborators репо `kuznetsov-kdv/CargoLogic`. Клон создан в `projects/cargologic/CargoLogic/`, настроен SSH-ключ. Старый снапшот (`CargoLogic-main`, 06.08.2026) сохранён. Активность в main: 691 коммит за 30 дней, последний `b661210` «Add ETRAN stub fallback for organization startup».
