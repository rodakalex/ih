# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import admin, start, questions, menu

logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.router,
        questions.router,
        menu.router,
        admin.router,
    )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
