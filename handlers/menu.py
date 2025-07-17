# handlers/menu.py
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards import get_profession_keyboard

router = Router()

@router.message(F.text.lower() == "главное меню")
async def handle_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите свою специальность:", reply_markup=get_profession_keyboard())
