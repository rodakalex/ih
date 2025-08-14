# main.py
import asyncio
import logging

from safe_send import patch_aiogram_senders

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import admin, start, questions, menu

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("bot")

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    patch_aiogram_senders(logger=logger, patch_bot_send_all=True)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.router,
        questions.router,
        menu.router,
        admin.router,
    )

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
