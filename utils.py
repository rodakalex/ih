# utils.py
import json
import os
from random import choice

QUESTIONS_FOLDER = "questions"

PROFESSION_FILES = {
    "1C Developer": "1c_developer.json",
    "Android Developer": "android.json",
    "Business Analyst": "business_analyst.json",
    "C/C++ Developer": "cpp.json",
    "C# Developer": "csharp.json",
    "Data Scientist": "datascience.json",
    "DevOps": "devops.json",
    "Flutter Developer": "flutter.json",
    "Frontend Developer": "frontend.json",
    "Golang Developer": "golang.json",
    "iOS Developer": "ios.json",
    "Java Developer": "java.json",
    "Machine Learning Engineer": "ml.json",
    "Node.js Developer": "nodejs.json",
    "PHP Developer": "php.json",
    "Product Manager": "product_manager.json",
    "Project Manager": "project_manager.json",
    "Python Developer": "python.json",
    "QA Engineer": "qa.json",
    "Ruby Developer": "ruby.json",
}

# utils.py
from sqlalchemy import select, func
from db import SessionLocal, Question

def load_questions_for_profession(profession: str) -> list[dict]:
    with SessionLocal() as db:
        rows = db.execute(
            select(Question).where(Question.profession == profession)
        ).scalars().all()

    if not rows:
        return [{"question": f"Пока нет вопросов для профессии {profession}.", "answer_html": None, "answer_text": None}]

    return [
        {"question": r.question, "answer_html": r.answer_html, "answer_text": r.answer_text}
        for r in rows
    ]

def get_random_question(profession: str) -> dict:
    with SessionLocal() as db:
        row = db.execute(
            select(Question)
            .where(Question.profession == profession)
            .order_by(func.random())
            .limit(1)
        ).scalar_one_or_none()

    if not row:
        return {"question": f"Пока нет вопросов для профессии {profession}.", "answer_html": None, "answer_text": None}

    return {"question": row.question, "answer_html": row.answer_html, "answer_text": row.answer_text}

def get_gpt_answer_from_question_text(profession: str, question_text: str) -> str:
    with SessionLocal() as db:
        row = db.execute(
            select(Question).where(
                Question.profession == profession,
                Question.question == question_text
            )
        ).scalar_one_or_none()

    if not row:
        return "❌ Не удалось найти ответ на этот вопрос."
    return row.answer_html or row.answer_text or "❌ К сожалению, подробный ответ отсутствует."
