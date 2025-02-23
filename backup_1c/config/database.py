"""Работа с базой данных."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backup_1c.config.config import config

logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Генератор сессий для работы с базой."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
