"""
Сопоставление ответа пользователя с эталонным.
Многоуровневый подход: exact → contains → synonym → keywords.
"""
import json
import re
from pathlib import Path

STOP_WORDS = {"это", "является", "процесс", "который", "что", "как", "для", "или", "и", "в", "на"}
KEYWORD_THRESHOLD = 0.4  # минимум 40% ключевых слов


def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[.,!?\-:;\"']", " ", s)
    s = " ".join(s.split())
    return s


def get_keywords(text: str) -> set[str]:
    words = set(re.findall(r"[а-яёa-z0-9]+", text.lower()))
    return words - STOP_WORDS


def load_synonyms(path: Path | None) -> dict[str, list[str]]:
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def expand_with_synonyms(text: str, synonyms: dict[str, list[str]]) -> set[str]:
    tokens = set(re.findall(r"[а-яёa-z0-9]+", text.lower()))
    for word, alts in synonyms.items():
        if word in tokens or any(a in text.lower() for a in alts):
            tokens.add(word)
            tokens.update(alts)
    return tokens


def check_match(user_answer: str, correct_answer: str, alternatives: list[str] | None, synonyms: dict) -> bool:
    user_n = normalize(user_answer)
    correct_n = normalize(correct_answer)

    if not user_n:
        return False

    # 1. exact match
    if user_n == correct_n:
        return True

    # 2. alternatives
    if alternatives:
        for alt in alternatives:
            if user_n == normalize(alt):
                return True

    # 3. contains (user in correct or correct in user)
    if correct_n in user_n or user_n in correct_n:
        return True

    # 4. synonym-expanded contains
    user_tokens = expand_with_synonyms(user_answer, synonyms)
    correct_tokens = expand_with_synonyms(correct_answer, synonyms)
    if user_tokens & correct_tokens and len(user_tokens & correct_tokens) >= 1:
        # ключевое слово есть
        pass

    # 5. keyword match
    correct_keys = get_keywords(correct_answer)
    if not correct_keys:
        return False
    user_keys = get_keywords(user_answer)
    overlap = len(correct_keys & user_keys) / len(correct_keys)
    if overlap >= KEYWORD_THRESHOLD:
        return True

    # 6. alternatives keyword match
    if alternatives:
        for alt in alternatives:
            alt_keys = get_keywords(alt)
            if alt_keys and len(alt_keys & user_keys) / len(alt_keys) >= KEYWORD_THRESHOLD:
                return True

    return False
