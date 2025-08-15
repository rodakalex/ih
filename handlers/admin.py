# handlers/admin.py
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils import get_question_by_id
from aiogram.filters import Command

# ⚠️ Установите свой пароль
ADMIN_PASSWORD = "supersecret"

# Храним список авторизованных админов
authorized_admins = set()

router = Router()

@router.message(Command("get_question"))
async def get_question(message: types.Message):
    if message.from_user.id not in authorized_admins:
        return await message.answer("⛔ У вас нет прав")

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("Использование: /get_question <id>")

    q_id = int(parts[1])
    q = get_question_by_id(q_id)

    if not q:
        return await message.answer(f"❌ Вопрос с ID {q_id} не найден")

    await message.answer(
        f"<b>Вопрос #{q.id}</b>\n\n<b>Текст:</b> {q.question}\n\n<b>Ответ:</b> {q.answer_text}",
        parse_mode="HTML"
    )


class AdminState(StatesGroup):
    waiting_for_password = State()

@router.message(F.text.lower() == "/admin")
async def admin_entry(message: types.Message, state: FSMContext):
    if message.from_user.id in authorized_admins:
        await message.answer("Добро пожаловать в админ-панель!")
        return
    await state.set_state(AdminState.waiting_for_password)
    await message.answer("Введите пароль:")

@router.message(AdminState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        authorized_admins.add(message.from_user.id)
        await state.clear()
        await message.answer("Доступ разрешён. Добро пожаловать в админ-панель!")
        # Здесь можно показать меню админа
    else:
        await state.clear()
        await message.answer("❌ Неверный пароль. Попробуйте снова через /admin.")
