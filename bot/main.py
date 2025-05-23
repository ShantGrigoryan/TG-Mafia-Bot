import asyncio
import logging
from aiogram import Bot, Dispatcher 
from aiogram.filters import CommandStart , Command
from aiogram.types import Message
from bot.config import BOT_TOKEN
from bot.handlers.group import router as group_router
from bot.handlers.private import router as private_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(group_router)
dp.include_router(private_router)




@dp.message(Command("test"))
async def cmd_start(message: Message):
    await message.answer("Привет! Это бот для игры в Мафию. Напиши /start в личке, чтобы начать.")


async def main():
    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())