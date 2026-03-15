# DevOps Quiz — навык для Яндекс Алисы

Викторина по DevOps (Linux, Docker, сети, Git, Kubernetes и др.) для навыка Алисы.

## Репозиторий

git@github.com:Mosl1k/devops.git

## Структура

```
devops/
  app/           # Flask webhook
  data/          # questions.json, synonyms.json
  scripts/       # parse_md.py — парсер .md → questions.json
  docker/
  kpalch-integration/  # Django app devops_quiz для копирования в kpalch
```

## Источник вопросов

`.md` из репозитория sobes (блоки `<details><summary>Q</summary>A</details>`).

Генерация `questions.json`:
```bash
python scripts/parse_md.py
```

## Запуск (Docker Compose)

```bash
cd docker
docker-compose up -d
```

Webhook: `http://localhost:2112/` (для продакшена — Nginx, путь `/skill/devops/`).

## Деплой на kpalch.ru

На сервере (vdska):

```bash
# Клонировать devops
git clone git@github.com:Mosl1k/devops.git /root/devops
cd /root/devops

# Создать .env из .env.example
cp .env.example .env
# Добавить DATABASE_URL при необходимости (для PostgreSQL)

# Деплой
sudo KPALCH_ROOT=/root/gestalt DEVOPS_ROOT=/root/devops ./scripts/deploy-to-kpalch.sh
```

Скрипт: добавляет Redis (devops-redis), поднимает alice-devops на порту 2113, патчит nginx (location /skill/devops/). Существующий alice (список покупок) на 2112 не затрагивается.

## Интеграция в kpalch (код)

1. Скопировать `kpalch-integration/devops_quiz/` в `kpalch/backend/`
2. Добавить `devops_quiz` в `INSTALLED_APPS`
3. `python manage.py migrate`
4. `python manage.py load_devops_questions --source=/path/to/questions.json --clear`
5. Добавить сервис `alice-devops` в docker-compose, `location /skill/devops/` в nginx

Подробнее: [kpalch-integration/README.md](kpalch-integration/README.md)

## Переменные окружения

- `REDIS_URL` / `REDIS_ADDR` — Redis для сессий
- `QUESTIONS_PATH` — путь к questions.json (по умолчанию `data/questions.json`)
- `DATABASE_URL` — опционально, читать вопросы из PostgreSQL (таблица `devops_quiz_quizquestion`)

## Протокол Алисы

- POST `/` — webhook, JSON в формате [протокола Алисы](https://yandex.ru/dev/dialogs/alice/doc/ru/)
- Ответ ≤ 4.5 сек, HTTPS для продакшена
