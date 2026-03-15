#!/bin/bash
# Деплой DevOps Quiz на сервер рядом с kpalch.
# Запускать на сервере: sudo ./scripts/deploy-to-kpalch.sh
# Переменные: KPALCH_ROOT, DEVOPS_ROOT. Секреты — из .env (не коммитить).
set -e

KPALCH_ROOT="${KPALCH_ROOT:-/root/gestalt}"
DEVOPS_ROOT="${DEVOPS_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
ENV_FILE="${DEVOPS_ROOT}/.env"

echo "DEVOPS_ROOT=$DEVOPS_ROOT"
echo "KPALCH_ROOT=$KPALCH_ROOT"

if [ ! -f "$ENV_FILE" ]; then
    echo "Создайте .env: cp .env.example .env (может быть пустым при использовании JSON)"
    exit 1
fi

# Сеть kpalch
NETWORK="gestalt_network"

# 1. Redis (если ещё нет)
if ! docker ps -a --format '{{.Names}}' | grep -qx devops-redis; then
    echo "Запуск Redis..."
    docker run -d --name devops-redis \
        --network "$NETWORK" \
        --restart unless-stopped \
        redis:7-alpine
fi

# 2. Сборка и запуск alice-devops
cd "$DEVOPS_ROOT"
docker build -f docker/Dockerfile -t alice-devops:latest .

# Остановить старый контейнер если есть
docker stop alice-devops 2>/dev/null || true
docker rm alice-devops 2>/dev/null || true

docker run -d --name alice-devops \
    --network "$NETWORK" \
    --restart unless-stopped \
    -e REDIS_URL="redis://devops-redis:6379/0" \
    -e PORT=2113 \
    -e QUESTIONS_PATH=/app/data/questions.json \
    -v "$DEVOPS_ROOT/data:/app/data:ro" \
    --env-file "$ENV_FILE" \
    alice-devops:latest

# 3. Патч nginx — добавить location /skill/devops/
NGINX_CONF="${KPALCH_ROOT}/infra/nginx/nginx.conf"
BACKUP="${NGINX_CONF}.bak.$(date +%Y%m%d%H%M%S)"

if ! grep -q "location /skill/devops/" "$NGINX_CONF"; then
    echo "Добавляем location /skill/devops/ в nginx..."
    cp "$NGINX_CONF" "$BACKUP"
    INSERT_FILE="${DEVOPS_ROOT}/scripts/nginx-devops-insert.conf"
    # Вставить блок перед "# Проксирование на alice"
    awk '
        /# Проксирование на alice \(Python Flask\)/ && !done {
            system("cat \"'"$INSERT_FILE"'\"")
            done=1
        }
        {print}
    ' "$NGINX_CONF" > "${NGINX_CONF}.tmp" && mv "${NGINX_CONF}.tmp" "$NGINX_CONF"
fi

# 4. Перезагрузка nginx
docker exec nginx nginx -t && docker exec nginx nginx -s reload

echo "Готово. Webhook: https://kpalch.ru/skill/devops/"
