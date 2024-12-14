import os
import datetime

from dotenv import load_dotenv


# Мой ID пользователя
BASE_VK_USER_ID = '240664024'

# Абсолютный путь к папке results, где по умолчанию будут храниться результаты
RESULTS_BASE_DIR = os.path.join(os.path.dirname(__file__), 'results')

BASE_RESULT_FILE = os.path.join(RESULTS_BASE_DIR, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.json')

# Записываем варианты адресов API, если не сработает один, будет обращение по второму
SERVER_ADDRESS_OPTIONS = ['api.vk.com', 'api.vk.ru']

# Протестированная версия VK API
TESTED_VK_API_VERSION = '5.199'

# Время между выполнением запросов, чтобы не возникало ошибки слишком частых обращений
API_SLEEP_TIME = 0.3

# Получаем токен API из файла .env
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Максимальная глуина прохода по фолловерам и подпискам пользователя
MAX_API_DEPTH = 2

# Путь к папке с логами
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
