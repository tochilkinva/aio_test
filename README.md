### Описание
Асинхронный бот Telegram с функцией получения новостей от 3dnews.

### Алгоритм работы
Каждые 30 минут получаем новости с https://3dnews.ru/news/.

Парсим их и записываем в базу со статусом непрочитано.

По команде /news отправляем в канал 5 постов и меняем им статус на прочитано.

Если все посты прочитаны, то говорим, что нет новых постов.

### Команды
- /start - Появляется при первом старте бота
- /news - Выводит 5 непрочитанных новостей 

### Технологии
aiogram, aiosqlite, aiohttp, apscheduler, beatifulsoap

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tochilkinva/aio_test.git
cd aio_test
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
. env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл .env и укажите необходимые данные.
Пример есть в .env_example.
Затем просто запустите код aio_bot_parser.py в Python.

### Автор
Валентин
