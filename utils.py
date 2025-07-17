import json
import os
from config import QUESTIONS_FOLDER, PROFESSION_FILES

def load_questions_for_profession(profession: str) -> list:
    filename = PROFESSION_FILES.get(profession)
    if not filename:
        print(f"[!] Нет файла вопросов для профессии: {profession}")
        return [{"question": f"Пока нет вопросов для профессии {profession}."}]
    
    path = os.path.join(QUESTIONS_FOLDER, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                raise ValueError("Файл пуст")
            return data
    except Exception as e:
        print(f"[!] Ошибка при загрузке {filename}: {e}")
        return [{"question": f"Ошибка при загрузке вопросов для {profession}."}]

def get_random_question(profession: str) -> str:
    from random import choice
    questions = load_questions_for_profession(profession)
    q = choice(questions)
    return f"Вопрос для {profession}:\n{q['question']}"
