# Project Systematisator 2.0

> Методология организации проектов для AI-ассистентов (Claude Code, Cursor, Copilot).

**Экономия токенов + модульная архитектура + автоматизация**

---

## Что нового в v2.0

| Фича | Описание |
|------|----------|
| **Модульные правила** | `.agents/reference/` — загружай только нужное |
| **Компактный CLAUDE.md** | Роутинг вместо всего контента |
| **"When to Read"** | Явная колонка когда что читать |
| **MCP интеграция** | Memory, PostgreSQL, Context7 |
| **Hooks** | Автоматизация (защита .env, уведомления) |
| **Без номеров строк** | grep паттерны вместо устаревающих строк |

---

## Быстрый старт

```bash
# Клонируй
git clone https://github.com/lamawuf/project-systematisator.git

# Скопируй шаблоны в свой проект
cp -r project-systematisator/templates/v2/* your-project/
```

---

## Структура проекта (v2.0)

```
YOUR_PROJECT/
├── CLAUDE.md                    # Навигация (компактный!)
├── .claude/
│   ├── project.skills.md        # Философия проекта
│   └── settings.json            # Hooks
├── .agents/
│   ├── AGENTS.md                # Список модулей
│   └── reference/
│       ├── commands.md          # Модуль: команды
│       ├── payments.md          # Модуль: платежи
│       └── database.md          # Модуль: БД
└── docs/                        # Документация для людей
```

---

## Ключевая идея

**Было:**
```
CLAUDE.md (175 строк) → Claude читает ВСЁ
```

**Стало:**
```
CLAUDE.md (50 строк) → роутинг
    ↓
.agents/reference/payments.md → только если работаешь с платежами
```

**Результат:** Контекст остаётся "lean" (чистым)

---

## Документация

- **[METHODOLOGY-v2.md](METHODOLOGY-v2.md)** — Полная методология
- **[templates/v2/](templates/v2/)** — Шаблоны файлов
- **[examples/](examples/)** — Примеры проектов

---

## MCP серверы (рекомендуемые)

```bash
# Memory — память между сессиями
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory

# PostgreSQL — SQL запросы напрямую
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://..."
```

---

## Экономия

| Метрика | v1.0 | v2.0 |
|---------|------|------|
| CLAUDE.md | ~1800 токенов | ~500 токенов |
| На сессию | ~3100 токенов | ~1800-2300 токенов |
| Экономия | — | ~800 токенов/сессия |

---

## Автор

Telegram: [@psclama](https://t.me/psclama)
YouTube: [Lama Drops](https://youtube.com/@ruslanllama)

---

## Лицензия

MIT

---

*v2.0 | 2026-01-19*
