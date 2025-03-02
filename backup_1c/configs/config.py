"""Файл для работы с переменными окружения."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Хранение переменных окружения."""

    LOG_PATH: str = os.getenv("LOG_PATH", "logs/app.log")
    TEMP_PATH: str = os.getenv("TEMP_PATH", "tmp")
    DB_PATH: str = os.getenv("DB_PATH", "app.sqlite3")
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    BACKUP_PATH: str = os.getenv("BACKUP_PATH", "backup")
    ENTERPRISE_PATH: str = os.getenv("ENTERPRISE_PATH", "/opt/1cv8/x86_64/")
    ENTERPRISE_VERSION: Optional[str] = os.getenv("ENTERPRISE_VERSION")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DBMS: str = os.getenv("DBMS", "PostgreSQL")
    DB_USER: str = os.getenv("DB_USER") or ""
    DB_PASS: str = os.getenv("DB_PASS") or ""
    BACKUP_FILE_LIFETIME: int = int(os.getenv("BACKUP_FILE_LIFETIME", 90))
    YANDEX_DISK_TOKEN: str = os.getenv("YANDEX_DISK_TOKEN", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    def __post_init__(self):
        """Проверка переменных окружения."""
        if not self.DB_USER or not self.DB_PASS:
            raise ValueError("DB_USER и DB_PASS должны быть указаны")


config = Config()
