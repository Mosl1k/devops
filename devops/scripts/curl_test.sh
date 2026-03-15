#!/bin/bash
# Тест webhook через curl. Сессия test-curl-N (уникальная)
BASE="https://kpalch.ru/skill/devops"
SID="test-curl-$(date +%s)"

post() {
  curl -s -X POST "$BASE" -H "Content-Type: application/json" \
    -d "{\"session\":{\"session_id\":\"$SID\",\"message_id\":1},\"request\":{\"command\":\"$1\"}}"
}

echo "=== 1. линукс ==="
post "линукс"
echo ""
echo ""

echo "=== 2. Ответ: runlevel (про runlevels) ==="
post "runlevel"
echo ""
echo ""

echo "=== 3. Ответ: ps (про статусы процессов) ==="
post "ps"
echo ""
echo ""

echo "=== 4. Ответ: proc (про /proc) ==="
post "proc"
echo ""
echo ""

echo "=== 5. Ответ: df (про диск) ==="
post "df"
echo ""
echo ""
