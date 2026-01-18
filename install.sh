#!/bin/bash
#
# Project Systematisator — установка
#
# Использование:
#   git clone https://github.com/USERNAME/project-systematisator.git
#   cd project-systematisator
#   bash install.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "🚀 Установка Project Systematisator"
echo ""

# Создаём ~/.claude если нет
mkdir -p "$CLAUDE_DIR/templates"
mkdir -p "$CLAUDE_DIR/scripts"

# Копируем global skills
if [ -f "$CLAUDE_DIR/global.skills.md" ]; then
    echo "⚠️  ~/.claude/global.skills.md уже существует"
    read -p "   Перезаписать? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$SCRIPT_DIR/global.skills.md" "$CLAUDE_DIR/global.skills.md"
        echo "✅ Обновлён global.skills.md"
    else
        echo "   Пропущено"
    fi
else
    cp "$SCRIPT_DIR/global.skills.md" "$CLAUDE_DIR/global.skills.md"
    echo "✅ Установлен ~/.claude/global.skills.md"
fi

# Копируем шаблоны
cp "$SCRIPT_DIR/templates/"* "$CLAUDE_DIR/templates/"
echo "✅ Установлены шаблоны в ~/.claude/templates/"

# Копируем скрипты
cp "$SCRIPT_DIR/scripts/"* "$CLAUDE_DIR/scripts/"
chmod +x "$CLAUDE_DIR/scripts/"*
echo "✅ Установлены скрипты в ~/.claude/scripts/"

echo ""
echo "🎉 Готово!"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Использование:"
echo ""
echo "  1. В любом проекте запусти:"
echo ""
echo "     bash ~/.claude/templates/init-project.sh \"МойПроект\""
echo ""
echo "  2. Это создаст:"
echo "     • CLAUDE.md — навигация для AI"
echo "     • .claude/project.skills.md — философия проекта"
echo "     • .claude/settings.local.json — permissions"
echo ""
echo "  3. Заполни CLAUDE.md роутингом задач"
echo ""
echo "  4. Для больших файлов (>200 строк) сгенерируй индекс:"
echo ""
echo "     python ~/.claude/scripts/update-index.py src/lib/actions.ts"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
