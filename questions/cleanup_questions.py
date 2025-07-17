import json

INPUT_PATH = "./1c_developer_raw.json"
OUTPUT_PATH = "./1c_developer.json"

def clean_questions(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    cleaned = []
    for item in data:
        cleaned.append({
            "question": item.get("question", "").strip(),
            "answer": ""
        })

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(cleaned, outfile, ensure_ascii=False, indent=2)

    print(f"✅ Готово: сохранено {len(cleaned)} вопросов в {output_path}")

if __name__ == "__main__":
    clean_questions(INPUT_PATH, OUTPUT_PATH)
