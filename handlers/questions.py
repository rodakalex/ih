# handlers/questions.py
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils import (
    get_random_question,
    get_gpt_answer_from_question_text,
)
from keyboards import get_idk_keyboard, get_answer_keyboard, get_profession_keyboard
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data.startswith('prof_'))
async def handle_profession_choice(callback: types.CallbackQuery, state: FSMContext):
    profession = callback.data.split('_', 1)[1]
    question = get_random_question(profession)

    await state.update_data(
        profession=profession,
        last_question=question['question']
    )

    await callback.message.answer(
        question["question"],
        reply_markup=get_idk_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(F.text.lower() == "idk")
async def handle_idk_button(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profession = data.get("profession")
    question_text = data.get("last_question")

    logger.info(f"[IDK] User: {message.from_user.id}, Profession: {profession}, Question: {question_text}")

    if not profession or not question_text:
        logger.warning(f"[IDK] Missing state — profession or question is None")
        await message.answer(
            "⚠️ Не найден текущий вопрос. Попробуй начать с выбора профессии",
            reply_markup=get_profession_keyboard(),
            parse_mode="HTML"
        )
        return

    answer = get_gpt_answer_from_question_text(profession, question_text)
    if not answer:
        logger.warning(f"[IDK] No answer found for question: {question_text}")
    else:
        logger.debug(f"[IDK] Answer found: {answer[:80]}...")

    try:
        await message.answer(
            answer,
            reply_markup=get_answer_keyboard(),
            parse_mode="HTML"
        )
        logger.info(f"[IDK] Message sent successfully.")
    except Exception as e:
        logger.exception(f"[IDK] message: {raw_text}")
        logger.exception(f"[IDK] Failed to send message: {e}")


@router.message(F.text.lower() == "следующий вопрос")
async def handle_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profession = data.get('profession')

    if not profession:
        await message.answer(
            "⚠️ Вы ещё не выбрали профессию. Пожалуйста, вернитесь в главное меню.",
            reply_markup=get_profession_keyboard(),
            parse_mode="HTML"
        )
        return

    question = get_random_question(profession)

    await state.update_data(last_question=question['question'])

    await message.answer(
        question,
        reply_markup=get_idk_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text.lower() == "поясни подробнее")
async def handle_more(message: types.Message):
    await message.answer(
        "🔍 Мокнутый подробный ответ от GPT",
        parse_mode="HTML"
    )
