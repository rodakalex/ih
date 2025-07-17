# main.py
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, questions, menu

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(
    start.router,
    questions.router,
    menu.router,
)

if __name__ == '__main__':
    dp.run_polling(bot)
