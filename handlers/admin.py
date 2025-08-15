# handlers/admin.py
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# ⚠️ Установите свой пароль
ADMIN_PASSWORD = "supersecret"

# Храним список авторизованных админов
authorized_admins = set()

router = Router()

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
