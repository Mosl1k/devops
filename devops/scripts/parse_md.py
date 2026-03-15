#!/usr/bin/env python3
"""
Парсер .md файлов sobes: извлекает Q/A из <details><summary>Q</summary>A</details>.
Результат: data/questions.json
"""
import json
import re
import sys
from pathlib import Path

# маппинг файл -> category
FILE_TO_CATEGORY = {
    "Linux.md": "linux",
    "Containers.md": "docker",
    "Networks.md": "networks",
    "Git.md": "git",
    "CI-CD.md": "cicd",
    "Monitoring.md": "monitoring",
    "IaC.md": "iac",
    "Kubernetes.md": "kubernetes",
    "AWS.md": "aws",
    "Databases.md": "databases",
    "Python.md": "python",
    "Debug.md": "debug",
    "Hardware.md": "hardware",
}

# стоп-слова для сокращения ответа (начало предложения)
STOP_PHRASES = ["Источник:", "См. также", "Подробнее:"]


def strip_markdown(text: str) -> str:
    """Убрать Markdown-разметку."""
    # **bold** -> bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    # *italic* -> italic
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    # `code` -> code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # ссылки [text](url)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def shorten_answer(text: str, max_len: int = 200) -> str:
    """Сократить ответ до 1-2 предложений."""
    text = text.strip()
    for phrase in STOP_PHRASES:
        idx = text.find(phrase)
        if idx != -1:
            text = text[:idx]
    text = strip_markdown(text)
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    # обрезать по последнему предложению до max_len
    cut = text[: max_len + 1]
    last_dot = cut.rfind(".")
    if last_dot > max_len // 2:
        return text[: last_dot + 1]
    return text[:max_len].rsplit(" ", 1)[0] + "."


def extract_qa(content: str) -> list[tuple[str, str]]:
    """Извлечь пары (вопрос, ответ) из <details> блоков."""
    pattern = re.compile(
        r"<details>\s*<summary>([^<]+)</summary>\s*(.*?)</details>",
        re.DOTALL,
    )
    pairs = []
    for m in pattern.finditer(content):
        q = m.group(1).strip()
        a = m.group(2).strip()
        if q and a:
            pairs.append((q, a))
    return pairs


def main():
    # путь к sobes .md (родитель devops)
    base = Path(__file__).resolve().parent.parent.parent
    data_dir = base / "devops" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    questions = []
    for filename, category in FILE_TO_CATEGORY.items():
        md_path = base / filename
        if not md_path.exists():
            print(f"Skip (not found): {filename}", file=sys.stderr)
            continue
        content = md_path.read_text(encoding="utf-8")
        pairs = extract_qa(content)
        for i, (q, a) in enumerate(pairs):
            qid = f"{category}-{i + 1:03d}"
            questions.append(
                {
                    "id": qid,
                    "category": category,
                    "question": q,
                    "answer": shorten_answer(a),
                }
            )
        print(f"{filename}: {len(pairs)} questions -> {category}")

    out = {
        "skill": "devops",
        "version": "1.0",
        "questions": questions,
    }
    out_path = data_dir / "questions.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_path} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
