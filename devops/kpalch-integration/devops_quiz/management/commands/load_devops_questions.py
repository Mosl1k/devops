"""
Загрузить вопросы в БД из JSON.
Использование: python manage.py load_devops_questions --source=/path/to/questions.json
Или: python manage.py load_devops_questions  (по умолчанию ищет data/questions.json)
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from devops_quiz.models import QuizQuestion


class Command(BaseCommand):
    help = "Load DevOps quiz questions from JSON into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            default=None,
            help="Path to questions.json (default: ../../data/questions.json)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing questions before loading",
        )

    def handle(self, *args, **options):
        source = options.get("source")
        if source:
            path = Path(source)
        else:
            self.stderr.write(self.style.ERROR("Use --source=/path/to/questions.json"))
            return
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        data = json.loads(path.read_text(encoding="utf-8"))
        questions = data.get("questions", [])

        if options.get("clear"):
            deleted, _ = QuizQuestion.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing questions")

        created = 0
        for q in questions:
            obj, _ = QuizQuestion.objects.update_or_create(
                id=q["id"],
                defaults={
                    "category": q.get("category", ""),
                    "question": q.get("question", ""),
                    "answer": q.get("answer", ""),
                },
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {created} questions from {path}"))
