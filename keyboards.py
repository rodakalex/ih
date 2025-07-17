# keyboards.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

PROFESSIONS = [
    "1C Developer", "Android Developer", "Business Analyst", "C/C++ Developer", "C# Developer",
    "Data Scientist", "DevOps", "Flutter Developer", "Frontend Developer", "Golang Developer",
    "iOS Developer", "Java Developer", "Machine Learning Engineer", "Node.js Developer",
    "PHP Developer", "Product Manager", "Project Manager", "Python Developer", "QA Engineer",
    "Ruby Developer"
]

def get_profession_keyboard():
    builder = InlineKeyboardBuilder()
    for p in PROFESSIONS:
        builder.button(text=p, callback_data=f"prof_{p}")
    builder.adjust(3)
    return builder.as_markup()

def get_idk_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="idk")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_answer_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Следующий вопрос")],
            [types.KeyboardButton(text="Поясни подробнее")],
            [types.KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
