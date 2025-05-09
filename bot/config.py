import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env

# env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv()

# Основные настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройки базы данных (для SQLite или PostgreSQL)
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # По умолчанию SQLite
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'mafia_bot.db')
POSTGRES_DSN = os.getenv('POSTGRES_DSN', 'postgresql://user:password@localhost:5432/mafia_db')

# Настройки игры
MIN_PLAYERS = int(os.getenv('MIN_PLAYERS', 5))  # Минимальное количество игроков
MAX_MAFIA = int(os.getenv('MAX_MAFIA', 2))     # Максимальное количество мафии