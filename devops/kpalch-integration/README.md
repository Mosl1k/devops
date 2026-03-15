# Интеграция devops_quiz в kpalch

Скопировать `devops_quiz/` в `kpalch/backend/`.

В `gestalt/settings.py` добавить в `INSTALLED_APPS`:
```python
'devops_quiz',
```

Миграции:
```bash
python manage.py makemigrations devops_quiz
python manage.py migrate
```

Загрузить вопросы (один раз):
```bash
python manage.py load_devops_questions --source=/path/to/devops/data/questions.json --clear
```
