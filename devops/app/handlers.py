"""
State machine и интенты для DevOps-викторины.
"""
import json
import random
from pathlib import Path

from .matcher import check_match

TOPIC_ALIASES = {"линукс": "linux", "докер": "docker", "сети": "networks", "гит": "git", "кубер": "kubernetes"}
CATEGORIES = {
    "linux": "Linux",
    "docker": "Docker",
    "networks": "Сети",
    "git": "Git",
    "cicd": "CI/CD",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "databases": "Базы данных",
    "python": "Python",
    "monitoring": "Мониторинг",
    "iac": "IaC (Ansible, Terraform)",
    "debug": "Debug",
    "hardware": "Железо",
}

ADD_TRIGGERS = ("добавить вопрос", "новый вопрос", "добавь вопрос")
NEXT_TRIGGERS = ("следующий", "следующий вопрос", "дальше")
CHANGE_TOPIC_TRIGGERS = ("другая тема", "сменить тему", "смена темы", "другая")
REPEAT_TRIGGERS = ("повтори", "ещё раз", "повтори вопрос")


def load_questions_from_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("questions", [])


def load_questions(questions_path: Path | None, db_questions: list[dict] | None = None) -> list[dict]:
    if db_questions:
        return db_questions
    if questions_path and questions_path.exists():
        return load_questions_from_json(questions_path)
    return []


def get_questions_by_category(questions: list[dict], category: str | None) -> list[dict]:
    if not category or category == "all":
        return questions
    return [q for q in questions if q.get("category") == category]


RELATED_CATEGORIES = {
    "linux": ["Сети", "Docker"],
    "networks": ["Linux", "Docker"],
    "docker": ["Linux", "Kubernetes"],
    "kubernetes": ["Docker", "Linux"],
    "debug": ["Linux", "Базы данных"],
    "hardware": ["Linux"],
}

def pick_random_question(questions: list[dict], exclude_ids: set[str] | None = None) -> dict | None:
    exclude_ids = exclude_ids or set()
    pool = [q for q in questions if q.get("id") not in exclude_ids]
    return random.choice(pool) if pool else None


def pick_next_question(
    questions: list[dict],
    category: str | None,
    current_q: dict | None,
    answered_ids: set[str],
) -> dict | None:
    """Следующий вопрос: предпочитать follow_up, исключать уже отвеченные."""
    pool = get_questions_by_category(questions, category)
    pool_ids = {q["id"] for q in pool}
    if current_q and current_q.get("follow_up_ids"):
        for fid in current_q["follow_up_ids"]:
            if fid not in answered_ids and fid in pool_ids:
                return next((q for q in questions if q["id"] == fid), None)
    return pick_random_question(pool, answered_ids)


def detect_intent(text: str, phase: str) -> str:
    t = text.lower().strip()
    if phase == "add_question":
        return "add_input"
    if any(trigger in t for trigger in ADD_TRIGGERS):
        return "add_question"
    if phase == "quiz" and any(trigger in t for trigger in NEXT_TRIGGERS):
        return "next"
    if any(trigger in t for trigger in CHANGE_TOPIC_TRIGGERS):
        return "change_topic"
    if phase == "quiz" and any(trigger in t for trigger in REPEAT_TRIGGERS):
        return "repeat"
    for cat_key, cat_name in CATEGORIES.items():
        if cat_key in t or cat_name.lower() in t:
            return "choose_topic"
    if "все" in t or "все темы" in t or "микс" in t:
        return "choose_topic"
    if phase == "choosing_topic":
        return "choose_topic"
    if phase == "quiz":
        return "answer"
    if phase == "add_question":
        return "add_input"
    return "unknown"


def resolve_topic(t: str) -> str | None:
    t = t.lower().strip()
    if "все" in t or "микс" in t:
        return "all"
    for alias, cat_key in TOPIC_ALIASES.items():
        if alias in t:
            return cat_key
    for cat_key, cat_name in CATEGORIES.items():
        if cat_key in t or cat_name.lower() in t:
            return cat_key
    return None


def handle(
    text: str,
    session: dict,
    questions: list[dict],
    synonyms: dict,
) -> tuple[str, dict]:
    phase = session.get("phase", "welcome")
    category = session.get("category")
    current = session.get("current_question")
    add_buffer = session.get("add_buffer", {})

    intent = detect_intent(text, phase)

    # add_question mode
    if intent == "add_question" or phase == "add_question":
        return _handle_add_question(text, session, intent, add_buffer, questions)

    # next / change_topic / repeat
    if intent == "next":
        session["phase"] = "quiz"
        answered = set(session.get("answered_ids", []))
        pool = get_questions_by_category(questions, category)
        exclude = answered | ({current} if current else set())
        q = pick_random_question(pool, exclude_ids=exclude)
        if q:
            session["current_question"] = q["id"]
            return _question_line(q, category, "Вопрос"), session
        return _suggest_other_topic(category), session

    if intent == "repeat" and current:
        q = next((x for x in questions if x["id"] == current), None)
        if q:
            qt = _tts(q["question"], q, "question")
            if category == "all" and q.get("category"):
                cat_name = CATEGORIES.get(q["category"], q["category"])
                return f"Повторяю. Из темы {cat_name}: {qt}", session
            return f"Повторяю: {qt}", session
        return "Не могу повторить. Скажи «следующий» для нового вопроса.", session

    if intent == "change_topic":
        session["phase"] = "choosing_topic"
        session["category"] = None
        session["current_question"] = None
        session["answered_ids"] = []
        cats = ", ".join(CATEGORIES.values())
        return f"Выбери тему: {cats}. Или скажи «все темы».", session

    # choose topic
    if phase == "choosing_topic" or phase == "welcome":
        topic = resolve_topic(text)
        if topic is None and phase == "welcome":
            cats = ", ".join(CATEGORIES.values())
            return f"Привет! DevOps-викторина. Выбери тему: {cats}. Или скажи «все темы».", session
        if topic is None:
            return "Не понял тему. Назови: Linux, Docker, Сети и т.д.", session
        session["phase"] = "quiz"
        session["category"] = topic
        session["answered_ids"] = []
        pool = get_questions_by_category(questions, topic)
        if not pool:
            return "В этой теме пока нет вопросов. Выбери другую.", session
        q = pick_random_question(pool)
        session["current_question"] = q["id"]
        return f"Тема выбрана. " + _question_line(q, topic, "Вопрос"), session

    # answer
    if phase == "quiz" and current:
        q = next((x for x in questions if x["id"] == current), None)
        if not q:
            return "Ошибка. Скажи «следующий».", session
        ok = check_match(text, q["answer"], q.get("answer_alternatives"), synonyms)
        answered = set(session.get("answered_ids", []))
        answered.add(q["id"])
        session["answered_ids"] = list(answered)
        session["current_question"] = None
        nq = pick_next_question(questions, category, q, answered)
        if ok:
            if nq:
                session["current_question"] = nq["id"]
                return f"Правильно! " + _question_line(nq, category, "Следующий вопрос"), session
            return _suggest_other_topic(category), session
        if nq:
            session["current_question"] = nq["id"]
            ans = _tts(q["answer"], q, "answer")
            return f"Нет. Правильно: {ans}. " + _question_line(nq, category, "Следующий вопрос"), session
        ans = _tts(q["answer"], q, "answer")
        return f"Нет. Правильно: {ans}. {_suggest_other_topic(category)}", session

    return "Скажи «следующий» или «другая тема».", session


def _tts(text: str, q: dict, key: str) -> str:
    """Текст для озвучки: приоритет *_tts (без слэшей/букв), иначе как есть."""
    return q.get(f"{key}_tts", text)


def _question_line(q: dict, category: str | None, prefix: str = "Вопрос") -> str:
    """Формирует строку с вопросом. При «все темы» добавляет название темы."""
    qt = _tts(q["question"], q, "question")
    if category == "all" and q.get("category"):
        cat_name = CATEGORIES.get(q["category"], q["category"])
        return f"{prefix} из темы {cat_name}: {qt}"
    return f"{prefix}: {qt}"


def _suggest_other_topic(category: str | None) -> str:
    """Предложить другую тему вместо повторения."""
    if category and category in RELATED_CATEGORIES:
        topics = ", ".join(RELATED_CATEGORIES[category][:2])
        return f"Вопросы закончились. Можем перейти к {topics}. Назови тему."
    return "Вопросы закончились. Скажи «другая тема» или название темы."


def _handle_add_question(text: str, session: dict, intent: str, add_buffer: dict, questions: list[dict]) -> tuple[str, dict]:
    session["phase"] = "add_question"
    if intent == "add_question":
        session["add_buffer"] = {}
        return "К какой теме относится — linux, docker, сети и т.д.? Или «своя тема».", session

    if "topic" not in add_buffer:
        topic = resolve_topic(text)
        if topic and topic != "all":
            add_buffer["topic"] = topic
            session["add_buffer"] = add_buffer
            return "Скажи вопрос.", session
        add_buffer["topic"] = "custom"
        session["add_buffer"] = add_buffer
        return "Скажи вопрос.", session

    if "question" not in add_buffer:
        add_buffer["question"] = text.strip()
        session["add_buffer"] = add_buffer
        return "Теперь скажи правильный ответ.", session

    add_buffer["answer"] = text.strip()
    session["add_buffer"] = add_buffer
    topic = add_buffer.get("topic", "custom")
    qid = f"{topic}-custom-{len([x for x in questions if x.get('category') == topic]) + 1}"
    snippet = json.dumps(
        {"id": qid, "category": topic, "question": add_buffer["question"], "answer": add_buffer["answer"]},
        ensure_ascii=False,
    )
    session["phase"] = "quiz"
    session["add_buffer"] = {}
    return f"Запиши и добавь в questions.json: {snippet}. Готово!", session
