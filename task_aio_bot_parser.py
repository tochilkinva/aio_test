"""
Простой пример создания бота Telegram с функцией получения новостей с сайта 3dnews
Стэк: aiogram, asyncio, beatifulsoap
"""
import asyncio
import os
import logging

from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink

from aiohttp import ClientSession
from dotenv import load_dotenv
from task6 import parse_posts

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN) # Объект бота
dp = Dispatcher(bot) # Диспетчер для бота

# Включаем логирование. Пишем логи в файл example.log
logging.basicConfig(
    filename='task_aio_bot_parser.log',
    level=logging.DEBUG,
)



async def get_news() -> str:
    """
    Запрашиваем новости с 3dnews.ru и возвращаем HTML
    :return: str
    """
    async with ClientSession() as session:
        url = f'https://3dnews.ru/news/'
        async with session.get(url=url) as response:
            html_response = await response.text()
            return html_response

async def get_and_parse_news() -> dict:
    """Парсим HTML и возвращаем dict
    :return: dict[post_number] = (
        post_text.text,
        post_href)
    """
    posts_html = await get_news() 
    posts_dict = parse_posts(posts_html)
    return posts_dict


# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    posts_dict = await get_and_parse_news()
    for key, value in posts_dict.items():
        await message.answer(hlink(value[0], value[1]), parse_mode="HTML", disable_web_page_preview=False)


@dp.message_handler(commands='news')
async def cmd_news(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Свежее", "Позднее"]
    keyboard.add(*buttons)
    await message.answer("Выберите свежие или поздние новости?", reply_markup=keyboard)

@dp.message_handler(Text(equals="Свежее"))
async def cmd_news_fresh(message: types.Message):
    await message.reply("Отличный выбор! Свежее")

@dp.message_handler(Text(equals="Позднее"))
async def cmd_news_later(message: types.Message):
    await message.reply("Отличный выбор! Позднее")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Привет! Это CrazyBot, давай почитаем новости с 3DNews!")
    await cmd_news(message=message)

@dp.message_handler(commands="help")
async def cmd_help(message: types.Message): 
    await cmd_start(message=message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) # Запуск бота


