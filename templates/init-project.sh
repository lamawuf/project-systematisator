#!/bin/bash
#
# Инициализация структуры Claude для нового проекта
#
# Использование:
#   ~/.claude/templates/init-project.sh "ProjectName"
#
# Или из любой директории:
#   bash ~/.claude/templates/init-project.sh "ProjectName"
#

PROJECT_NAME="${1:-NewProject}"
DATE=$(date +%Y-%m-%d)
TEMPLATES_DIR="$HOME/.claude/templates"

echo "🚀 Инициализация проекта: $PROJECT_NAME"

# Создаём директорию .claude
mkdir -p .claude

# Копируем и заполняем CLAUDE.md
if [ ! -f "CLAUDE.md" ]; then
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{DATE}}/$DATE/g" \
        -e "s/{{MAIN_FILE}}/actions.ts/g" \
        "$TEMPLATES_DIR/CLAUDE.md.template" > CLAUDE.md
    echo "✅ Создан CLAUDE.md"
else
    echo "⚠️  CLAUDE.md уже существует, пропускаю"
fi

# Копируем и заполняем project.skills.md
if [ ! -f ".claude/project.skills.md" ]; then
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{DATE}}/$DATE/g" \
        "$TEMPLATES_DIR/project.skills.md.template" > .claude/project.skills.md
    echo "✅ Создан .claude/project.skills.md"
else
    echo "⚠️  .claude/project.skills.md уже существует, пропускаю"
fi

# Создаём базовый settings.local.json
if [ ! -f ".claude/settings.local.json" ]; then
    cat > .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(npm install:*)",
      "Bash(npm run dev)",
      "Bash(npm run build:*)",
      "Bash(npx prisma generate:*)",
      "Bash(npx prisma db push:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "WebSearch"
    ]
  }
}
EOF
    echo "✅ Создан .claude/settings.local.json"
else
    echo "⚠️  .claude/settings.local.json уже существует, пропускаю"
fi

echo ""
echo "🎉 Готово! Структура создана:"
echo "   CLAUDE.md"
echo "   .claude/project.skills.md"
echo "   .claude/settings.local.json"
echo ""
echo "Следующие шаги:"
echo "1. Заполни CLAUDE.md роутингом задач"
echo "2. Опиши философию в .claude/project.skills.md"
echo "3. Добавь нужные permissions в settings.local.json"
