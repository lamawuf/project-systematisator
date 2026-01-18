#!/usr/bin/env python3
"""
Скрипт для автообновления индексов функций в CLAUDE.md

Парсит TypeScript/Python файлы и выводит функции с номерами строк.
Результат можно вставить в CLAUDE.md.

Использование:
    python scripts/update-index.py src/lib/actions.ts
    python scripts/update-index.py bot_logic.py
    python scripts/update-index.py --all  # все большие файлы
"""

import re
import sys
import os
from pathlib import Path

# Настрой под свой проект: файлы >200 строк
BIG_FILES = [
    # "src/lib/actions.ts",
    # "src/lib/credits.ts",
    # "bot_logic.py",
]

def extract_exports_ts(filepath: str) -> list[tuple[str, int, str]]:
    """
    Извлекает экспортируемые функции/типы из TypeScript файла.
    Возвращает: [(имя, номер_строки, тип), ...]
    """
    exports = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    patterns = [
        (r'^export async function (\w+)', 'async fn'),
        (r'^export function (\w+)', 'fn'),
        (r'^export type (\w+)', 'type'),
        (r'^export interface (\w+)', 'interface'),
        (r'^export const (\w+)', 'const'),
    ]

    for i, line in enumerate(lines, 1):
        for pattern, kind in patterns:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                exports.append((name, i, kind))
                break

    return exports

def extract_functions_py(filepath: str) -> list[tuple[str, int, str]]:
    """
    Извлекает функции и классы из Python файла.
    Возвращает: [(имя, номер_строки, тип), ...]
    """
    functions = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    patterns = [
        (r'^async def (\w+)', 'async fn'),
        (r'^def (\w+)', 'fn'),
        (r'^class (\w+)', 'class'),
    ]

    for i, line in enumerate(lines, 1):
        for pattern, kind in patterns:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                functions.append((name, i, kind))
                break

    return functions

def extract_all(filepath: str) -> list[tuple[str, int, str]]:
    """Определяет тип файла и извлекает функции."""
    if filepath.endswith('.py'):
        return extract_functions_py(filepath)
    elif filepath.endswith(('.ts', '.tsx', '.js', '.jsx')):
        return extract_exports_ts(filepath)
    else:
        print(f"Неизвестный тип файла: {filepath}")
        return []

def format_markdown_table(exports: list[tuple[str, int, str]], filepath: str) -> str:
    """Форматирует результат как Markdown таблицу."""

    with open(filepath, 'r', encoding='utf-8') as f:
        line_count = len(f.readlines())

    filename = os.path.basename(filepath)

    lines = [
        f"## Индекс {filename} ({line_count} строк)",
        "",
        "| Функция/Тип | Строка | Назначение |",
        "|-------------|--------|------------|",
    ]

    for name, line_num, kind in exports:
        desc = guess_description(name, kind)
        lines.append(f"| `{name}` | {line_num} | {desc} |")

    return "\n".join(lines)

def guess_description(name: str, kind: str) -> str:
    """Пытается угадать описание по имени функции."""

    # Добавь свои специальные случаи
    descriptions = {
        # 'sendMessage': 'Отправка сообщения',
        # 'runAgent': '**Главная** — запуск агента',
    }

    if name in descriptions:
        return descriptions[name]

    # Паттерны
    if name.startswith('delete'):
        return f"Удалить {name[6:].lower()}"
    if name.startswith('create'):
        return f"Создать {name[6:].lower()}"
    if name.startswith('move'):
        return "Перемещение"
    if name.startswith('toggle'):
        return "Переключить статус"
    if name.startswith('get'):
        return "Получить данные"
    if name.startswith('set'):
        return "Установить значение"
    if name.startswith('cmd_'):
        return f"Команда /{name[4:]}"
    if name.startswith('callback_'):
        return f"Callback: {name[9:]}"

    if kind == 'type':
        return "Тип"
    if kind == 'interface':
        return "Интерфейс"
    if kind == 'const':
        return "Константа"
    if kind == 'class':
        return "Класс"

    return "—"

def find_big_files(directory: str = ".", min_lines: int = 200) -> list[str]:
    """Находит все файлы больше min_lines строк."""
    big_files = []

    for root, dirs, files in os.walk(directory):
        # Пропускаем node_modules, venv, .git и т.д.
        dirs[:] = [d for d in dirs if d not in ('node_modules', 'venv', '.venv', '.git', '__pycache__', 'dist', 'build')]

        for file in files:
            if file.endswith(('.py', '.ts', '.tsx', '.js', '.jsx')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    if lines >= min_lines:
                        big_files.append((filepath, lines))
                except:
                    pass

    return sorted(big_files, key=lambda x: -x[1])

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python scripts/update-index.py <файл>")
        print("  python scripts/update-index.py --all")
        print("  python scripts/update-index.py --find  # найти большие файлы")
        sys.exit(1)

    if sys.argv[1] == '--find':
        print("Большие файлы (>200 строк):\n")
        for filepath, lines in find_big_files():
            print(f"  {filepath} ({lines})")
        print("\nДобавь их в BIG_FILES в скрипте.")

    elif sys.argv[1] == '--all':
        if not BIG_FILES:
            print("BIG_FILES пуст. Запусти --find и добавь файлы.")
            sys.exit(1)

        for filepath in BIG_FILES:
            if os.path.exists(filepath):
                print(f"\n{'='*60}")
                exports = extract_all(filepath)
                print(format_markdown_table(exports, filepath))
            else:
                print(f"Файл не найден: {filepath}")
    else:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Файл не найден: {filepath}")
            sys.exit(1)

        exports = extract_all(filepath)
        print(format_markdown_table(exports, filepath))

if __name__ == '__main__':
    main()
