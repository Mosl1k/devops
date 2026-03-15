#!/usr/bin/env python3
"""
Тест matcher: какие вопросы не принимают короткие (1-2 слова) ответы.
Для провалов добавляем answer_alternatives.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.matcher import check_match, load_synonyms, get_keywords

DATA = Path(__file__).resolve().parent.parent / "data"
QUESTIONS = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))["questions"]
SYNONYMS = load_synonyms(DATA / "synonyms.json")


def extract_short_candidates(question: str, answer: str) -> list[str]:
    """Типичные короткие ответы (1-2 слова), которые пользователь мог бы сказать."""
    ans_lower = answer.lower()
    q_lower = question.lower()
    candidates = []
    # Словарь: если в вопросе/ответе есть ключ → добавить варианты ответа
    mapping = [
        ("runlevel", "target", "systemd", "уровень", "уровни"),
        ("proc", "/proc"),
        ("процесс", "процессы", "ps", "top"),
        ("статус", "статусы", "r", "s", "d", "z", "t", "ps"),
        ("зомби", "zombie"),
        ("сигнал", "сигналы", "sigterm", "sigkill"),
        ("systemd", "системд", "init"),
        ("posix", "стандарт"),
        ("df", "du"),
        ("mount", "маунт"),
        ("grub", "загрузчик"),
        ("bios", "uefi"),
        ("pxe", "сеть"),
        ("docker", "докер", "контейнер"),
        ("kubernetes", "k8s"),
        ("ansible", "terraform"),
        ("git", "коммит"),
        ("nginx", "apache"),
        ("postgresql", "postgres", "mysql"),
    ]
    for group in mapping:
        if any(k in ans_lower or k in q_lower for k in group):
            candidates.extend(group[:3])
    # Первые значимые слова из ответа
    words = re.findall(r"[а-яёa-z0-9/]+", ans_lower)
    stop = {"это", "для", "или", "и", "в", "на", "с", "по", "из", "от", "до", "не", "без", "что", "как"}
    for w in words:
        if len(w) >= 2 and w not in stop and w not in candidates:
            candidates.append(w)
            if len(candidates) >= 8:
                break
    return list(dict.fromkeys(candidates))[:8]


def main():
    fails = []
    for q in QUESTIONS:
        ans = q.get("answer", "")
        alts = q.get("answer_alternatives", [])
        short_tried = extract_short_candidates(q["question"], ans)
        any_ok = False
        for short in short_tried:
            if check_match(short, ans, alts, SYNONYMS):
                any_ok = True
                break
        if not any_ok and short_tried:
            fails.append({
                "id": q["id"],
                "question": q["question"][:60] + "..." if len(q["question"]) > 60 else q["question"],
                "answer": ans[:80] + "..." if len(ans) > 80 else ans,
                "short_tried": short_tried,
                "keywords": list(get_keywords(ans))[:10],
            })

    print(f"Провалено {len(fails)} из {len(QUESTIONS)} вопросов при коротких ответах:\n")
    for f in fails:
        print(f"ID: {f['id']}")
        print(f"  Q: {f['question']}")
        print(f"  Пробовали: {f['short_tried']}")
        print(f"  Ключевые: {f['keywords']}")
        print()
    return fails


if __name__ == "__main__":
    main()
