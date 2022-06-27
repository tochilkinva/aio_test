"""
Простой пример создания бота Telegram
"""

import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


bot = Bot(token=TELEGRAM_TOKEN) # Объект бота
dp = Dispatcher(bot) # Диспетчер для бота

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO) 

# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    await message.reply("Test")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply("Привет! Это CrazyBot! Давай веселиться!")

@dp.message_handler(commands="help")
async def cmd_start(message: types.Message):
    await message.reply("Привет! Это CrazyBot! Давай веселиться!")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
