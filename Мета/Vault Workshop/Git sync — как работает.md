---
type: vault_infrastructure
title: "Git sync — как работает vault на VM ↔ GitHub ↔ Mac"
status: active
version: 1.0
created: 2026-10-01
updated: 2026-10-01
authors: ["Pablo"]
tags: [infrastructure, git, obsidian, sync]
---

# 🔄 Git sync — как работает vault

Это **единственный источник истины** про то, как vault синхронизируется между VM, GitHub и Mac. Если ты агент — читай этот файл перед любой операцией с git в vault.

## 📐 Архитектура

```
┌─────────────────────┐          ┌─────────────────────┐          ┌─────────────────────┐
│  VM (Pablo-агенты)  │  push    │     GitHub          │  pull    │   Mac (Obsidian)    │
│                     │ ───────► │                     │ ◄─────── │                     │
│  /home/work/...     │          │  PavelD1711/        │          │  Obsidian Git       │
│  /vaults/dodon/     │  pull    │  Dodon_Vault_Real   │  push    │  plugin             │
│                     │ ◄─────── │  (private)          │ ───────► │  (ручной)           │
└─────────────────────┘          └─────────────────────┘          └─────────────────────┘
```

GitHub — **единая точка синхронизации.** Прямой коннект VM↔Mac отсутствует.

---

## 🔑 Авторизация

### На VM — SSH (не HTTPS, не PAT)

```
Remote: git@github-dodon-vault:PavelD1711/Dodon_Vault_Real.git
SSH key: ~/.ssh/github_dodon_vault
SSH config: Host github-dodon-vault → HostName github.com, IdentityFile ~/.ssh/github_dodon_vault
```

**НЕ нужен** Personal Access Token (PAT), HTTPS, пароль — ничего. SSH-ключ уже сконфигурирован и работает.

### На Mac — Obsidian Git plugin

Плагин использует системный git с настроенными credentials мака (может быть SSH-ключ, GitHub Desktop, 1Password credential helper и т.д.) — это зона Павла. Если плагин не может пушить — Павел разбирается с настройкой git на маке.

---

## ⚙️ Поведение

### На VM — ручное (команды агента)

Коммит + push делает агент явно:

```bash
cd /home/work/.openclaw/workspace/vaults/dodon
git pull --rebase origin main    # всегда перед работой
# ... вносим изменения ...
git add -A
git commit -m "Pablo: краткое описание"
git push origin main             # SSH, работает без доп. настройки
```

**Автоматики на VM нет** — ни крона, ни webhook'а.

### На Mac — автоматика Obsidian Git

Конфиг плагина (`.obsidian/plugins/obsidian-git/data.json`):

| Параметр | Значение | Что делает |
|----------|----------|------------|
| `autoSaveInterval` | 10 минут | Автокоммит локальных изменений |
| `autoPullInterval` | **5 минут** | **Автоматически тянет с GitHub** |
| `autoPushInterval` | **0 (выключен)** | **Автопуша нет** — только ручной |
| `pullBeforePush` | true | Перед push всегда pull |
| `syncMethod` | merge | При конфликте — merge |

**Следствия:**
- Что я (агент на VM) запушил в GitHub → **через 0–5 минут окажется в твоём Obsidian на маке автоматически.**
- Что ты изменил на маке → **автоматически не уйдёт** на GitHub. Нужно ручное: `Cmd+Shift+P` → `Obsidian Git: Commit-and-sync` или кнопка в sidebar.

---

## 🚦 Типовые сценарии

### Сценарий 1 — Агент добавляет файл в vault

```bash
cd /home/work/.openclaw/workspace/vaults/dodon
git pull --rebase origin main
# создаём/правим файл
git add Проекты/900.1\ Интеграция\ оператора.md
git commit -m "Pablo-ПО: #900.1 Интеграция оператора и финотдела (draft)"
git push origin main
```

На маке у Павла автоматически через ≤5 минут. Готово.

### Сценарий 2 — Павел правит файл в Obsidian на маке

Мак не автопушит. Варианты:
- **A.** Павел нажимает в Obsidian `Cmd+P` → `Obsidian Git: Commit-and-sync`
- **B.** Павел в терминале на маке: `git add -A && git commit -m "..." && git push`

После этого на VM: `git pull --rebase` подтянет изменения.

### Сценарий 3 — Параллельные правки (мак + VM)

- VM коммит + push
- На маке autoPull через ≤5 мин → мерж (`syncMethod: merge`)
- Если конфликт — Obsidian покажет modal, Павел разруливает

---

## 🔧 Диагностика проблем push

### «Push не проходит» → проверь по чек-листу:

```bash
cd /home/work/.openclaw/workspace/vaults/dodon

# 1. Что говорит статус?
git status

# 2. Куда настроен remote?
git remote -v
# Должно быть: origin  git@github-dodon-vault:PavelD1711/Dodon_Vault_Real.git (push)

# 3. Есть ли SSH-ключ?
ls -la ~/.ssh/github_dodon_vault
cat ~/.ssh/config | grep -A 3 github-dodon-vault

# 4. Проверка SSH-коннекта
ssh -T git@github-dodon-vault
# Должно вернуть: "Hi PavelD1711! You've successfully authenticated..."

# 5. Dry-run push
git push --dry-run origin main
# Если "Everything up-to-date" — всё ок, push технически работает

# 6. Что отличается от origin?
git fetch origin
git rev-list --left-right --count main...origin/main
# "N  0" = локально N коммитов не запушено
# "0  M" = на origin M коммитов не вытянуто
# "0  0" = в синхроне
```

### Частые ошибки и причины

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Permission denied (publickey)` | SSH-ключ не загружен или сломан | Проверить `~/.ssh/github_dodon_vault`, права `chmod 600`, SSH-config |
| `could not read Username for 'https://...` | Remote случайно переключён на HTTPS | `git remote set-url origin git@github-dodon-vault:PavelD1711/Dodon_Vault_Real.git` |
| `Updates were rejected because the tip of your current branch is behind` | На origin новее коммиты | `git pull --rebase origin main`, затем `git push` |
| `fatal: refusing to merge unrelated histories` | Vault переинициализирован | Разбираться вручную, не делать `--allow-unrelated-histories` без согласования |

### ❌ НЕ надо делать:
- Переключать remote на HTTPS и просить у Павла PAT — **SSH уже настроен, работает**
- Делать `git push -f` без явного согласия Павла — может затереть изменения с мака
- Делать `git reset --hard origin/main` без бэкапа — удалит локальные изменения

---

## 🤖 Правила для агентов

1. **Перед любой работой в vault:** `git pull --rebase origin main`
2. **После каждого смыслового блока работы:** `git add -A && git commit -m "..." && git push`
3. **Сообщение коммита:** `Pablo[-роль]: краткое описание` (например `Pablo-ПО: #001 активный`)
4. **Не копить** 20 правок без push — чем мельче атомы, тем проще откат
5. **НЕ просить у Павла PAT/HTTPS-токен** — SSH уже работает
6. **Если push провалился** — пройди диагностику выше, определи причину, пиши в чат с конкретной ошибкой (не «не могу»)

---

## 📝 История изменений

- **2026-10-01** — v1.0 создан после кейса в Проектном офисе `-5324519714`: Pablo-ПО утром просил у Павла GitHub PAT, не зная что remote на SSH и работает. Pablo-DM разобрался, задокументировал.
