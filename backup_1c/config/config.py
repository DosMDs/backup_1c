"""Файл для работы с переменными окружения."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Хранение переменных окружения."""

    LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
    TEMP_PATH = os.getenv("TEMP_PATH", "tmp")
    DB_PATH = os.getenv("DB_PATH", "app.sqlite3")
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    BACKUP_PATH = os.getenv("BACKUP_PATH", "/backup")
    # Данные для ibcmd
    DB_SERVER = os.getenv("DB_SERVER")
    DBMS = os.getenv("DMBS", "PostgreSQL")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")

    def __init__(self):
        """Инициализация класса Config."""
        if not self.DB_SERVER:
            raise ValueError("DB_SERVER не установлен")
        if not self.DB_USER or not self.DB_PASS:
            raise ValueError("DB_USER или DB_PASS не установлены")


config = Config()
