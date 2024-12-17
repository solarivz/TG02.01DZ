import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator
from config import TOKEN


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("aiogram")

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# ================= Хэндлеры ================= #

# 1. Хэндлер для команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         "Я сохраню твои фото, отправлю голосовые сообщения и переводу текст на английский язык.")




# ================= Запуск бота ================= #
async def main():
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был остановлен!")
