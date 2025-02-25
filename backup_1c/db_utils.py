"""Методы для работы с данными."""

from datetime import datetime, timezone
from typing import List, Optional

from backup_1c.configs.config import config
from backup_1c.configs.database import FileStatus, get_db
from backup_1c.models import DatabaseCreds, File
from backup_1c.utils import calculate_threshold_date, delete_file
from backup_1c.yadisk_utils import (
    delete_file_from_yadisk,
    empty_trash,
    upload_file_to_yadisk,
)


def get_all_database_creds() -> List[DatabaseCreds]:
    """Получает список всех баз данных из таблицы database_creds."""
    db = next(get_db())
    creds_list = db.query(DatabaseCreds).all()  # Запрашиваем все записи
    return creds_list


def add_file(full_path: str) -> File:
    """Добавляет новый файл в базу данных."""
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
        file.status = new_status
        file.date_modified = datetime.now(timezone.utc)
        db.commit()


def get_files_by_status(status: FileStatus) -> List[File]:
    """Возвращает список файлов с указанным статусом."""
    if not isinstance(status, FileStatus):
        raise ValueError("Статус должен быть из FileStatus")
    db = next(get_db())
    file_list = db.query(File).filter(File.status == status).all()
    return file_list


def get_file_by_path(full_path: str) -> Optional[File]:
    """Возвращает файл по полному пути."""
    db = next(get_db())
    file = db.query(File).filter(File.full_path == full_path).first()
    return file


def delete_old_backups() -> None:
    """Удаляет файлы бэкапов, старше BACKUP_FILE_LIFETIME дней."""
    db = next(get_db())
    threshold_date = calculate_threshold_date(config.BACKUP_FILE_LIFETIME)

    old_files = (
        db.query(File)
        .filter(~File.is_deleted, File.date_added < threshold_date)
        .all()
    )

    for file in old_files:
        if delete_file(file.full_path):
            file.status = FileStatus.DELETED
            file.is_deleted = True
            file.date_modified = datetime.now(timezone.utc)  # Исправлено здесь
            db.commit()


def sync_new_files_to_yadisk() -> None:
    """Синхронизирует новые файлы с Яндекс.Диском."""
    db = next(get_db())
    new_files = (
        db.query(File)
        .filter(File.status == FileStatus.NEW, ~File.is_deleted)
        .all()
    )

    for file in new_files:
        file.status = FileStatus.SYNCING
        db.commit()

        download_link = upload_file_to_yadisk(file.full_path)
        if download_link:
            file.status = FileStatus.PROCESSED
            file.download_link = download_link
        else:
            file.status = FileStatus.NEW
        file.date_modified = datetime.now(timezone.utc)
        db.commit()


def sync_deleted_files_from_yadisk() -> None:
    """Удаляет файлы со статусом DELETING с Яндекс.Диска."""
    db = next(get_db())
    deleting_files = (
        db.query(File)
        .filter(File.status == FileStatus.DELETING, File.is_deleted)
        .all()
    )

    for file in deleting_files:
        file.status = FileStatus.SYNCING
        db.commit()

        if delete_file_from_yadisk(file.full_path):
            file.status = FileStatus.DELETED
            file.download_link = None
        else:
            file.status = FileStatus.DELETING
        file.date_modified = datetime.now(timezone.utc)
        db.commit()


def clear_yadisk_trash() -> None:
    """Очищает корзину на Яндекс.Диске."""
    empty_trash()
