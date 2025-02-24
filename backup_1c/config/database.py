"""Работа с базой данных."""

import enum
import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backup_1c.config.config import config

logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей базы данных."""

    pass


class FileStatus(enum.Enum):
    """Статусы файлов."""

    NEW = "New"
    SYNCING = "Syncing"
    PROCESSED = "Processed"
    DELETED = "Deleted"


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Генератор сессий для работы с базой."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
