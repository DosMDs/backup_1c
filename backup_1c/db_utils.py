"""Методы для работы с данными."""

import logging
from datetime import datetime
from typing import List, Optional

from backup_1c.config.database import FileStatus, get_db
from backup_1c.models import DatabaseCreds, File

logger = logging.getLogger(__name__)


def get_all_database_creds() -> List[DatabaseCreds]:
    """Получает список всех баз данных из таблицы database_creds."""
    logger.debug("Получение списка баз")
    db = next(get_db())
    creds_list = db.query(DatabaseCreds).all()  # Запрашиваем все записи
    logger.debug(f"Получено баз: {len(creds_list)}")
    return creds_list


def add_file(full_path: str) -> File:
    """Добавляет новый файл в базу данных."""
    logger.debug(f"Добавление файла: {full_path}, в базу")
    db = next(get_db())
    new_file = File(full_path=full_path)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def update_file_status(file_id: int, new_status: FileStatus) -> None:
    """Обновляет статус файла и дату изменения."""
    if not isinstance(new_status, FileStatus):
        raise ValueError("Статус должен быть из FileStatus")
    db = next(get_db())
    file = db.query(File).filter(File.id == file_id).first()
    if file:
        logger.debug(
            f"Изменение статуса файла: {file.full_path}, на {new_status}"
        )
        file.status = new_status
        file.date_modified = datetime.now(datetime.timezone.utc)
        db.commit()


def get_files_by_status(status: FileStatus) -> List[File]:
    """Возвращает список файлов с указанным статусом."""
    logger.debug(f"Получение списка файлов со статусом {status}")
    if not isinstance(status, FileStatus):
        raise ValueError("Статус должен быть из FileStatus")
    db = next(get_db())
    file_list = db.query(File).filter(File.status == status).all()
    logger.debug(f"Получено файлов: {len(file_list)}")
    return file_list


def get_file_by_path(full_path: str) -> Optional[File]:
    """Возвращает файл по полному пути."""
    logger.debug(f"Получение файла: {full_path}")
    db = next(get_db())
    file = db.query(File).filter(File.full_path == full_path).first()
    logger.debug(f"Получен файл: {file}")
    return file
