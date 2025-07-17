# handlers/start.py
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards import get_profession_keyboard

router = Router()

@router.message(F.text.lower().startswith('/start'))
async def show_start_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите свою специальность:", reply_markup=get_profession_keyboard())
