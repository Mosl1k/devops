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
    # Короткие ответы (1–2 символа) типа "l", "ip" не считать совпадением — слишком много ложных срабатываний
    MIN_LEN_FOR_CONTAINS = 3
    if correct_n in user_n:
        return True
    if len(user_n) >= MIN_LEN_FOR_CONTAINS and user_n in correct_n:
        return True

    # 4. synonym-expanded contains (совпадения длиной < 3 — отсеиваем, иначе "ip"/"l" дают ложные срабатывания)
    user_tokens = {t for t in expand_with_synonyms(user_answer, synonyms) if len(t) >= 2}
    correct_tokens = expand_with_synonyms(correct_answer, synonyms)
    overlap = user_tokens & correct_tokens
    if any(len(t) >= 3 for t in overlap):
        return True

    # 5. keyword match (with synonym expansion)
    correct_keys = get_keywords(correct_answer)
    if not correct_keys:
        return False
    correct_expanded = set(correct_keys)
    for k in correct_keys:
        correct_expanded.update(synonyms.get(k, []))
    user_keys = get_keywords(user_answer)
    user_expanded = set(user_keys)
    for k in user_keys:
        for kw, alts in synonyms.items():
            if k in alts or k == kw:
                user_expanded.add(kw)
                user_expanded.update(alts)
    overlap = len(correct_expanded & user_expanded) / len(correct_keys)
    if overlap >= KEYWORD_THRESHOLD:
        return True

    # 6. alternatives keyword match
    if alternatives:
        for alt in alternatives:
            alt_keys = get_keywords(alt)
            if alt_keys and len(alt_keys & user_keys) / len(alt_keys) >= KEYWORD_THRESHOLD:
                return True

    return False
