"""
Flask webhook для навыка Алисы «DevOps».
"""
import json
import os
from pathlib import Path

import redis
from flask import Flask, request, jsonify

from .handlers import handle
from .loader import load_questions

app = Flask(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
QUESTIONS_PATH = Path(os.getenv("QUESTIONS_PATH", str(DATA_DIR / "questions.json")))
REDIS_URL = os.getenv("REDIS_URL") or os.getenv("REDIS_ADDR", "redis://redis:6379/0")
SESSION_TTL = int(os.getenv("SESSION_TTL", 86400))  # 24h

_questions: list[dict] | None = None
_synonyms: dict | None = None


def get_questions() -> list[dict]:
    global _questions
    if _questions is None:
        _questions = load_questions(QUESTIONS_PATH)
    return _questions


def get_synonyms() -> dict:
    global _synonyms
    if _synonyms is None:
        from .matcher import load_synonyms as _load
        syn_path = DATA_DIR / "synonyms.json"
        _synonyms = _load(syn_path)
    return _synonyms


_session_store: dict = {}  # fallback if Redis unavailable


def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)


def get_session(session_id: str) -> dict:
    try:
        r = get_redis()
    except Exception:
        return _session_store.get(session_id, {})
    try:
        raw = r.get(f"devops_quiz:{session_id}")
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
    except Exception:
        return _session_store.get(session_id, {})
    return {}


def save_session(session_id: str, state: dict):
    try:
        r = get_redis()
        key = f"devops_quiz:{session_id}"
        r.setex(key, SESSION_TTL, json.dumps(state, ensure_ascii=False))
    except Exception:
        _session_store[session_id] = state


def _build_response(session: dict, text: str) -> dict:
    user_id = session.get("user_id") or (session.get("user") or {}).get("user_id")
    return {
        "version": "1.0",
        "session": {
            "message_id": session.get("message_id"),
            "session_id": session.get("session_id"),
            "skill_id": session.get("skill_id"),
            "user_id": user_id,
        },
        "response": {
            "text": text,
            "end_session": False,
        },
    }


@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json(silent=True)
    except Exception:
        data = None
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    session_data = data.get("session", {})
    session_id = session_data.get("session_id", "unknown")
    req = data.get("request", {}) or {}
    command = (req.get("command") or req.get("original_utterance") or "").strip()

    try:
        state = get_session(session_id)
        text, new_state = handle(
            command,
            state,
            get_questions(),
            get_synonyms(),
        )
        save_session(session_id, new_state)
        response = _build_response(session_data, text)
    except Exception as e:
        response = _build_response(
            session_data,
            "Произошла ошибка. Попробуйте ещё раз.",
        )
    return jsonify(response), 200


if __name__ in ("__main__", "app.main"):
    port = int(os.getenv("PORT", "2113"))
    app.run(host="0.0.0.0", port=port, debug=False)
