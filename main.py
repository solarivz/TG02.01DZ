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

# Хэндлер для команды /help
@dp.message(Command("help"))
async def help(message: Message):
    help_text = (
        "Доступные команды и функции бота:\n\n"
        "1. /start - Запустить бота и получить приветственное сообщение.\n"
        "2. /help - Показать список команд и их описание.\n"
        "3. /voice - Получить голосовое сообщение с заранее подготовленным текстом.\n\n"
        "Дополнительные функции:\n"
        "4. Отправьте фото - Бот сохранит ваше фото в папке `img` и подтвердит сохранение.\n"
        "5. Отправьте текст - Бот переведет ваш текст на английский язык и отправит результат.\n"
    )
    await message.answer(help_text)

# 2. Хэндлер для сохранения фото в папке img
@dp.message(F.photo)
async def save_photo(message: Message):
    # Получаем последнее фото в наилучшем качестве
    photo = message.photo[-1]
    # Скачиваем фото
    file_path = f"img/{photo.file_id}.jpg"
    await bot.download(photo, destination=file_path)
    await message.answer("Фото сохранено!")
    logger.info(f"Фото сохранено: {file_path}")

# 3. Хэндлер для отправки голосового сообщения (текст заранее подготовлен)
@dp.message(Command("voice"))
async def send_voice(message: Message):
    text = "Это голосовое сообщение отправлено ботом!"
    tts = gTTS(text=text, lang='ru')  # Генерируем голосовое сообщение
    tts.save("voice_message.ogg")     # Сохраняем в файл
    audio = FSInputFile("voice_message.ogg")
    await bot.send_voice(message.chat.id, voice=audio)
    os.remove("voice_message.ogg")  # Удаляем временный файл
    await message.answer("Голосовое сообщение отправлено!")

# 4. Хэндлер для перевода любого текста пользователя на английский язык
@dp.message(F.text)
async def translate_text(message: Message):
    original_text = message.text
    try:
        # Перевод текста на английский язык
        translation = translator.translate(original_text, dest='en')
        await message.answer(f"**Текст на английском:**\n{translation.text}")
    except Exception as e:
        logger.error(f"Ошибка перевода: {e}")
        await message.answer("Произошла ошибка при переводе текста. Попробуйте позже.")


# ================= Запуск бота ================= #
async def main():
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был остановлен!")
