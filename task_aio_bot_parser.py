"""
Простой пример создания бота Telegram с функцией получения новостей с сайта 3dnews
Стэк: aiogram, asyncio, beatifulsoap

Алгоритм работы
Каждые 30 минут получаем новости с https://3dnews.ru/news/.
Парсим их и записываем в базу со статусом не прочитано.
По команде /news отправляем в канал 5 постов и меняем им статус на прочитано.
Если все посты прочитаны, то о=говорим что нет постов.
"""

import os
import logging
import aiosqlite

from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.markdown import hlink

from aiohttp import ClientSession
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN) # Объект бота
dp = Dispatcher(bot) # Диспетчер для бота

# Включаем логирование. Пишем логи в файл example.log
logging.basicConfig(
    filename='task_aio_bot_parser.log',
    level=logging.DEBUG,
)

def parse_posts(raw_text: str) -> dict:
    """Парсим посты с 3dnews.ru
    arg: html as str
    return -> dict[post_number]: (post_text, post_href, post_img)
    """
    try:
        data = BeautifulSoup(raw_text, features='html.parser')
        posts = data.find_all('div', class_='article-entry')
        all_posts = {}
        for post in posts:
            post_number = int(post.get('id'))
            post_text = post.find('a', class_='entry-header')
            post_href = post_text.get("href")
            if post_href[:5] != 'https':
                post_href = f'https://3dnews.ru{post_href}'
            # post_img = post.find('img', class_='imageInAllFeed').get('src')
            # post_img = f'https://3dnews.ru{post_img}'
            all_posts[post_number] = (
                post_text.text,
                post_href,
                # post_img
            )
        return all_posts

    except Exception as e:
        raise Exception(
            f'Не удалось распарсить посты: {e}')

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

async def create_table() -> None:
    """
    Создаем таблицу для хранения постов
    """
    async with aiosqlite.connect('3dnews.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS posts'
                         '(post_id INTEGER PRIMARY KEY, title TEXT, url TEXT, status INTEGER, date TEXT)')
        await db.commit()

async def save_to_db(post_id, title, url) -> None:
    """
    Сохраняем пост в базу
    """
    async with aiosqlite.connect('3dnews.db') as db:
        try:
            await db.execute('INSERT INTO posts VALUES (?, ?, ?, ?, ?)',
                            (post_id, title, url, 0, datetime.now()))
            await db.commit()
        except:
            pass

async def load_new_posts() -> dict:
    """
    Загружаем 5 новых постов из базы и ставим им статус просмотренных
    :return -> None or dict[post_number]: (post_text, post_href)
    """
    result = {}
    async with aiosqlite.connect('3dnews.db') as db:
        async with db.execute('SELECT * FROM posts WHERE status = 0 LIMIT 5') as cursor:
            async for row in cursor:
                result[row[0]] = (row[1], row[2])
    if result == {}:
        return None

    for item in result:
        await set_post_status(item, 1)
    return result

async def set_post_status(post_id, status: int) -> None:
    """
    Поменять статус поста на status
    """
    async with aiosqlite.connect('3dnews.db') as db:
        await db.execute('UPDATE posts SET status = ? WHERE post_id = ?',
                        (status, post_id))
        await db.commit()

async def sched_get_news_to_db() -> None:
    """
    Функция для запроса постов и сохранения их в базе.
    Одинаковые посты не сохраняются
    """
    print('Get news and save to DB')
    posts_dict = await get_and_parse_news()
    for key, value in posts_dict.items():
        await save_to_db(key, value[0], value[1])


# Хэндлер на команду /news
@dp.message_handler(commands='news')
async def cmd_news(message: types.Message):
    new_posts = await load_new_posts()
    if new_posts is None:
        await message.answer("Новых постов еще нет")
    for key, value in new_posts.items():
        await message.answer(hlink(value[0], value[1]), parse_mode="HTML", disable_web_page_preview=False)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add("/news")

    await message.answer(
        "Привет! Это CrazyBot, давай почитаем новости с 3DNews!"
        "Отправь команду /news для получения новых постов",
        reply_markup=keyboard
    )


@dp.message_handler(commands="help")
async def cmd_help(message: types.Message): 
    await cmd_start(message=message)


async def on_startup_init(dp) -> None:
    """
    Создаем базу, если ее нет
    """
    await create_table() 


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()  # Запускаем расписание для записи постов с сайта
    scheduler.add_job(sched_get_news_to_db, 'interval', minutes=30)
    scheduler.start()

    executor.start_polling(dp, skip_updates=True , on_startup=on_startup_init) # Запуск бота
