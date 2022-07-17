"""
Простой пример работы асинхронных функций или корутин.
Main создает задачи, а затем через первый wait запускается выполнение корутин.
Каждая корутина возвращает результат.
Если использовать asyncio.gather, то в итоге будет список с результатом.
"""

import asyncio
import random
import time


async def get_weather(city):
    """Функция асинхронной задержки"""
    print(f'{city} start')
    await asyncio.sleep(random.random()*2)
    print(f'{city} done')
    return city


async def main(cities_):
    """Главная функция для запуска тасков"""
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))

    # result = await asyncio.gather(*tasks)  # result -> []
    # print(result)

    for task in tasks:
        result = await task
        print(f'{result} end')


if __name__ == '__main__':
    cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad',
              'Vladivostok', 'Minsk', 'Beijing', 'Delhi', 'Istanbul',
              'Tokyo', 'London', 'New York']

    print(time.strftime('%X'))

    asyncio.run(main(cities))

    print(time.strftime('%X'))
