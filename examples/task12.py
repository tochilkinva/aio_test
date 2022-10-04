"""
Скачиваем файлы из интернета
"""
import os
import requests


TEMP_DIR = 'temp'
FILE_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip'


VOSK_MODEL = 'models/vosk/model'            # путь к STT модели Vosk
SILERO_MODEL = 'models/silero/model.pt'     # путь к TTS модели Silero
FFMPEG_PATH = 'models/ffmpeg/ffmpeg.exe'    # путь к ffmpeg

def download_file_by_url_to_dir(file_url:str, dir:str):
    """
    Создаем папки и скачиваем файл по URL.

    :arg file_url: str  URL ссылка на файл
    :arg dir: str       папки для сохранения
    """
    # Создаем папки
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    file_name = file_url.split(sep='/')[-1]
    dest_file_path = os.path.join(dir, file_name)

    # Скачиваем файл если его нет
    if not os.path.exists(dest_file_path):
        response = requests.get(file_url)

        # Если не нашли файл то исключение
        if response.status_code == 404:
            raise Exception('Не удалось скачать файл по URL')
        
        # Сохраняем файл
        open(dest_file_path, "wb").write(response.content)


def check_models():
    if not os.path.exists(VOSK_MODEL):
        raise Exception("Vosk: сохраните папку model в папку vosk")
    
    if not os.path.isfile(SILERO_MODEL):
        raise Exception("Silero: сохраните model.pt в папку silero")
    
    if not os.path.isfile(FFMPEG_PATH):
        raise Exception("Ffmpeg: сохраните ffmpeg.exe в папку ffmpeg")
    
    print("Проверка пройдена")

if __name__ == "__main__":
    # download_file_by_url_to_dir(FILE_URL, TEMP_DIR)
    check_models()
