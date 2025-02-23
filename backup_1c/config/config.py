"""Файл для работы с переменными окружения."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Хранение переменных окружения."""

    LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")


config = Config()
