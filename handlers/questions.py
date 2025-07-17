# handlers/questions.py
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils import get_random_question
from keyboards import get_idk_keyboard, get_answer_keyboard, get_profession_keyboard

router = Router()

@router.callback_query(lambda c: c.data.startswith('prof_'))
async def handle_profession_choice(callback: types.CallbackQuery, state: FSMContext):
    profession = callback.data.split('_', 1)[1]
    await state.update_data(profession=profession)
    await callback.message.answer(get_random_question(profession), reply_markup=get_idk_keyboard())
    await callback.answer()

@router.message(F.text.lower() == "idk")
async def handle_idk_button(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profession = data.get('profession', 'Python Developer')
    await message.answer(f"🔍 Ответ от GPT для {profession} пока не реализован.", reply_markup=get_answer_keyboard())

@router.message(F.text.lower() == "следующий вопрос")
async def handle_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profession = data.get('profession')

    if not profession:
        await message.answer("⚠️ Вы ещё не выбрали профессию. Пожалуйста, вернитесь в главное меню.", reply_markup=get_profession_keyboard())
        return

    await message.answer(get_random_question(profession), reply_markup=get_idk_keyboard())


@router.message(F.text.lower() == "поясни подробнее")
async def handle_more(message: types.Message):
    await message.answer("🔍 Мокнутый подробный ответ от GPT")
