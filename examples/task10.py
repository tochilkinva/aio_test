"""
конвертация ogg > wav и wav > ogg
"""


import subprocess
import tempfile
import os

def wav_to_ogg(in_filename=None):
    with tempfile.TemporaryFile() as temp_out_file:
        if not in_filename:
            raise Exception('Укажите путь и имя файла относительно ffmpeg.exe')

        # Запрос в командную строку для обращения к FFmpeg
        # ffmpeg -i audio.wav -acodec libvorbis audio.ogg
        out_filename = f'{in_filename}.ogg'
        command = [
            r'.\ffmpeg.exe',  # путь до ffmpeg.exe
            '-i', in_filename,
            '-acodec', 'libvorbis',
            f'{out_filename}'
        ]
        proc = subprocess.Popen(command, stdout=temp_out_file, stderr=subprocess.DEVNULL)
        proc.wait()
        temp_out_file.seek(0)
        # print('wav > ogg done')
        return out_filename


def ogg_to_wav(in_filename=None):
    with tempfile.TemporaryFile() as temp_out_file:
        if not in_filename:
            raise Exception('Укажите путь и имя файла относительно ffmpeg.exe')

        # Запрос в командную строку для обращения к FFmpeg
        # ffmpeg -i input.ogg -ar 16000 -ac 1 -c:a pcm_s16le output.wav
        out_filename = f'{in_filename}.wav'
        command = [
            r'.\ffmpeg.exe',  # путь до ffmpeg.exe
            '-i', in_filename,
            '-ar', '16000',
            '-ac', '1',
            '-c:a', 'pcm_s16le',
            f'{out_filename}'
        ]
        proc = subprocess.Popen(command, stdout=temp_out_file, stderr=subprocess.DEVNULL)
        proc.wait()
        temp_out_file.seek(0)
        # print('ogg > wav done')
        return out_filename

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

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename='task10.log',
    )

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply("Привет! Это CrazyBot! Давай веселиться!")



# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    out_filename = ogg_to_wav(in_filename=r'.\voices\test_111.ogg')

    # out_filename = wav_to_ogg(in_filename=r'.\voices\test_000.wav')
    
    path = Path("", out_filename)
    voice = InputFile(path)
    print('Voice send')
    await bot.send_voice(message.from_user.id, voice)
    await message.reply("Test")
    # os.remove(out_filename)




@dp.message_handler(content_types=[types.ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    path = Path("voices", f"{file_id}.ogg")
    await bot.download_file(file_path, destination=path)
    await message.reply("Голосовое получено")



if __name__ == "__main__":
    # # Запуск бота
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
