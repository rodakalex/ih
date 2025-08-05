# utils.py
import json
import os
from random import choice
from config import QUESTIONS_FOLDER, PROFESSION_FILES

def load_questions_for_profession(profession: str) -> list[dict]:
    filename = PROFESSION_FILES.get(profession)
    if not filename:
        print(f"[!] Нет файла вопросов для профессии: {profession}")
        return [{"question": f"Пока нет вопросов для профессии {profession}.", "answer": ""}]
    
    path = os.path.join(QUESTIONS_FOLDER, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                raise ValueError("Файл пуст")
            return data
    except Exception as e:
        print(f"[!] Ошибка при загрузке {filename}: {e}")
        return [{"question": f"Ошибка при загрузке вопросов для {profession}.", "answer": ""}]

def get_random_question(profession: str) -> dict:
    questions = load_questions_for_profession(profession)
    return choice(questions)

def format_question(profession: str, question_obj: dict) -> str:
    return f"Вопрос для {profession}:\n{question_obj['question']}"

def get_gpt_answer_from_question_text(profession: str, question_text: str) -> str:
    questions = load_questions_for_profession(profession)
    for q in questions:
        if q["question"] == question_text:
            return q.get("answer") or "❌ К сожалению, подробный ответ отсутствует."
    return "❌ Не удалось найти ответ на этот вопрос."

