"""Файл для работы с переменными окружения."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Хранение переменных окружения."""

    # LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
    # TEMP_PATH = os.getenv("TEMP_PATH", "tmp")
    # DB_PATH = os.getenv("DB_PATH", "app.sqlite3")
    # DATABASE_URL = f"sqlite:///{DB_PATH}"
    # BACKUP_PATH = os.getenv("BACKUP_PATH", "/backup")
    # # Данные для ibcmd
    # ENTERPRISE_PATH = os.getenv("ENTERPRISE_PATH", "/opt/1cv8/x86_64/")
    # ENTERPRISE_VERSION = os.getenv("ENTERPRISE_VERSION")
    # DB_SERVER = os.getenv("DB_SERVER", "localhost")
    # DBMS = os.getenv("DMBS", "PostgreSQL")
    # DB_USER = os.getenv("DB_USER")
    # DB_PASS = os.getenv("DB_PASS")

    def __init__(self) -> None:
        """Инициализация класса Config."""
        self.LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
        self.TEMP_PATH = os.getenv("TEMP_PATH", "tmp")
        self.DB_PATH = os.getenv("DB_PATH", "app.sqlite3")
        self.DATABASE_URL = f"sqlite:///{self.DB_PATH}"
        self.BACKUP_PATH = os.getenv("BACKUP_PATH", "backup")
        self.ENTERPRISE_PATH = os.getenv(
            "ENTERPRISE_PATH", "/opt/1cv8/x86_64/"
        )
        self.ENTERPRISE_VERSION = os.getenv("ENTERPRISE_VERSION")
        self.DB_SERVER = os.getenv("DB_SERVER", "localhost")
        self.DBMS = os.getenv("DMBS", "PostgreSQL")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.BACKUP_FILE_LIFETIME = int(os.getenv("BACKUP_FILE_LIFETIME", 90))

        if not self.DB_USER or not self.DB_PASS:
            raise ValueError("DB_USER или DB_PASS не установлены")


config = Config()
