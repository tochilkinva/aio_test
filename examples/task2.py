"""
Простой пример создания сервера на aiohttp для определения
погоды в городе и записи данных в базу
Пример запроса http://localhost:8080/weather?city=москва
"""


import asyncio
import json
import logging
from datetime import datetime

import aiosqlite
from aiohttp import ClientSession, web


async def create_table():
    """
    Создаем таблицу для хранения погоды, если не создана
    """
    async with aiosqlite.connect('weather.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS requests '
                         '(date text, city text, weather text)')
        await db.commit()


async def save_to_db(city, weather):
    """
    Сохраняем данные в базу
    """
    async with aiosqlite.connect('weather.db') as db:
        await db.execute('INSERT INTO requests VALUES (?, ?, ?)',
                         (datetime.now(), city, weather))
        await db.commit()


async def get_weather(city):
    """
    Запрашиваем погоду у сервиса openweathermap через json
    """
    async with ClientSession() as session:
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            try:
                return weather_json["weather"][0]["main"]
            except KeyError:
                return 'Нет данных'


async def get_translation(text, source, target):
    """
    Переводим текст через сервис libretranslate
    """
    logging.info(f'Поступил запрос на на перевод слова: {text}')

    async with ClientSession() as session:
        url = 'https://libretranslate.de/translate'

        data = {'q': text,
                'source': source,
                'target': target,
                'format': 'text'}

        async with session.post(url, json=data) as response:
            translate_json = await response.json()

            try:
                return translate_json['translatedText']
            except KeyError:
                logging.error(f'Невозможно получить перевод для слова: {text}')
                return text


async def handle(request):
    """
    Функция реагирующая на запрос погоды:  /weather?city=москва
    """
    city_ru = request.rel_url.query['city']

    logging.info(f'Поступил запрос на город: {city_ru}')

    city_en = await get_translation(city_ru, 'ru', 'en')
    weather_en = await get_weather(city_en)
    weather_ru = await get_translation(weather_en, 'en', 'ru')

    result = {'city': city_ru, 'weather': weather_ru}

    await save_to_db(city_ru, weather_ru)

    return web.Response(text=json.dumps(result, ensure_ascii=False))


async def handle_echo(request):
    """
    Функция возвращающая запрос обратно:  /echo
    """
    logging.info('Поступил запрос echo')

    test = await request.read()
    # message.chat.id, message.text

    result = {'request': test}

    # return web.Response(text=json.dumps(result, ensure_ascii=False))
    return web.Response(text=result)


async def main():
    """
    Запускаем север на http://localhost:8080/
    Тестовый запрос http://localhost:8080/weather?city=москва
    Эхо http://localhost:8080/echo
    """
    await create_table()
    app = web.Application()
    app.add_routes([web.get('/weather', handle)])
    app.add_routes([web.get('/echo', handle_echo)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    while True:
        await asyncio.sleep(3600)


# Пишем логи в файл example.log
logging.basicConfig(
    filename='example.log',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    asyncio.run(main())
