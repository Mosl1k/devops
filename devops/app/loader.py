"""
Загрузка вопросов: из JSON или PostgreSQL.
"""
import json
import os
from pathlib import Path


def load_from_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("questions", [])


def load_from_postgres() -> list[dict] | None:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return None
    try:
        import psycopg2
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, category, question, answer FROM devops_quiz_quizquestion"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {"id": r[0], "category": r[1], "question": r[2], "answer": r[3]}
            for r in rows
        ]
    except Exception:
        return None


def load_questions(questions_path: Path | None) -> list[dict]:
    db_q = load_from_postgres()
    if db_q:
        return db_q
    if questions_path and questions_path.exists():
        return load_from_json(questions_path)
    return []
