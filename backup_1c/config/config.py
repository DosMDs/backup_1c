"""Файл для работы с переменными окружения."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Хранение переменных окружения."""

    LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
    DB_PATH = os.getenv("DB_PATH", "app.sqlite3")
    DATABASE_URL = f"sqlite:///{DB_PATH}"


config = Config()
