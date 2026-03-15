from django.db import models


class QuizQuestion(models.Model):
    """Вопрос для DevOps-викторины Алисы."""

    id = models.SlugField(max_length=50, primary_key=True)
    category = models.CharField(max_length=50, db_index=True)
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = "Вопрос викторины"
        verbose_name_plural = "Вопросы викторины"
        ordering = ["category", "id"]

    def __str__(self):
        return f"{self.id}: {self.question[:50]}..."
