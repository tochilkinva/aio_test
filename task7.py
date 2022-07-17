# Создание базы постов
# id заголовок ссылка статус просмотрено или нет дата

import aiosqlite
import asyncio
import logging
from datetime import datetime

async def create_table():
    """
    Создаем таблицу для хранения постов
    """
    async with aiosqlite.connect('3dnews.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS posts'
                         '(post_id INTEGER PRIMARY KEY, title TEXT, url TEXT, status INTEGER, date TEXT)')
        await db.commit()


async def save_to_db(post_id, title, url):
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


async def load_new_posts():
    """
    Загружаем 5 новых постов из базы и ставим им статус просмотренных
    :return -> dict[post_number]: (post_text, post_href)
    """
    result = {}
    async with aiosqlite.connect('3dnews.db') as db:
        async with db.execute('SELECT * FROM posts WHERE status = 0 LIMIT 5') as cursor:
            async for row in cursor:
                result[row[0]] = (row[1], row[2])

    for item in result:
        await set_post_status(item, 1)
    return result


async def set_post_status(post_id, status: int):
    """
    Поменять статус поста на status
    """
    async with aiosqlite.connect('3dnews.db') as db:
        await db.execute('UPDATE posts SET status = ? WHERE post_id = ?',
                        (status, post_id))
        await db.commit()



async def main(db):
    """
    Запускаем
    """

    await create_table()
    # await save_to_db(222, 'titl2', 'www.test2.ru')
    result = await load_new_posts()
    print(result)

    while True:
        await asyncio.sleep(3600)


# Пишем логи в файл example.log
logging.basicConfig(
    filename='example.log',
    level=logging.DEBUG,
)


if __name__ == '__main__':
    asyncio.run(main())
