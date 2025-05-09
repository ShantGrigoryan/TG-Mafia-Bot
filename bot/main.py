import asyncio
import logging
from aiogram import Bot, Dispatcher 
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import BOT_TOKEN
from handlers.group import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(router)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Это бот для игры в Мафию. Напиши /start в личке, чтобы начать.")

async def test (message : Message):
    message.answer(message.chat.type)

async def main():
    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())