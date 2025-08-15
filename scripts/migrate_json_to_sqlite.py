from pathlib import Path
import json
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from db import SessionLocal, init_db, Question

QUESTIONS_FOLDER = Path("questions")

# Преобразуем имя файла -> название профессии
# Можно дополнять по мере появления файлов
NAME_MAP = {
    "python": "Python Developer",
    "1c_developer": "1C Developer",
    # "frontend": "Frontend Developer",
    # ...
}

def guess_profession(stem: str) -> str:
    # сначала по словарю
    if stem in NAME_MAP:
        return NAME_MAP[stem]
    # иначе — title-case по имени файла
    # "java_backend" -> "Java Backend"
    return stem.replace("_", " ").title()

def norm(s: str) -> str:
    return (s or "").strip()

def main():
    init_db()

    if not QUESTIONS_FOLDER.exists():
        raise SystemExit(f"Папка {QUESTIONS_FOLDER} не найдена")

    inserted = 0
    skipped = 0

    with SessionLocal() as db:
        for path in QUESTIONS_FOLDER.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(data, list):
                    print(f"[!] Пропуск {path.name} — ожидается список объектов")
                    continue
            except Exception as e:
                print(f"[!] Ошибка чтения {path.name}: {e}")
                continue

            profession = guess_profession(path.stem)

            seen_in_file = set()
            for rec in data:
                q_text = norm(rec.get("question"))
                if not q_text or q_text in seen_in_file:
                    skipped += 1
                    continue
                seen_in_file.add(q_text)

                stmt = sqlite_insert(Question).values(
                    profession=profession,
                    question=q_text,
                    answer_text=norm(rec.get("answer")),
                    # если уже готовишь HTML — положи сюда строку
                    answer_html=rec.get("answer_html"),
                ).on_conflict_do_nothing(
                    index_elements=["profession", "question"]
                )

                res = db.execute(stmt)
                if res.rowcount:
                    inserted += 1
                else:
                    skipped += 1

        db.commit()

    print(f"Готово. Добавлено: {inserted}, пропущено: {skipped}")

if __name__ == "__main__":
    main()
