"""
Бот Telegram получение/отправка голосового и аудио

Алгоритм
Отправка голосового боту - ответ текстом и сохранение на диске
Команда test - ответ голосовым

создание аудио через текст: 
    текст > ttsselero > wav > ogg > bot
распознование аудио  текст:
    ogg > wav > vosk > текст > bot
конвертация ogg > wav и wav > ogg
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from pathlib import Path
from aiogram.types.input_file import InputFile

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота

# Включаем логирование, чтобы не пропустить важные сообщения
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename='task9.log',
)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply("Привет! Это CrazyBot! Давай веселиться!")


# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    """
    Отправка файла ogg в чат по команде /test
    """
    voice_path = Path("voices", f"AwACAgIAAxkBAAIFgmLhg4zCDZjb2z9aqdDuQO3dGjEtAALlGgACxX8RS0ZXGP5OBTHpKQQ.ogg")
    voice_file = InputFile(voice_path)
    await bot.send_voice(message.from_user.id, voice_file)
    await message.reply("Test")


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    """
    При получении голосового сохраняем его в папку
    """
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = Path("voices", f"{file_id}.ogg")
    await bot.download_file(file_path, destination=destination)
    await message.reply("Голосовое получено")


if __name__ == "__main__":
    # Запуск бота
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
