"""Основная функциональность по выгрузке баз."""

import logging
from typing import List

from backup_1c.configs.config import config
from backup_1c.configs.database import FileStatus
from backup_1c.db_utils import (
    add_file,
    clear_yadisk_trash,
    delete_old_backups,
    get_all_database_creds,
    get_file_by_path,
    sync_deleted_files_from_yadisk,
    sync_new_files_to_yadisk,
    update_file_status,
)
from backup_1c.models import DatabaseCreds
from backup_1c.utils import run_ibcmd

logger = logging.getLogger(__name__)


def backup_1c() -> None:
    """Работа с бэкапами 1С."""
    creds_list: List[DatabaseCreds] = get_all_database_creds()
    for creds in creds_list:
        logger.info(f"Выгрузка базы {creds.db_name}")
        full_path = run_ibcmd(creds.db_name, creds.username, creds.password)
        if full_path:
            file = get_file_by_path(full_path)
            if file:
                update_file_status(file.id, FileStatus.NEW)
            else:
                add_file(full_path)
            logger.info(f"Выгрузка базы {creds.db_name} завершена")
        else:
            logger.error(f"База {creds.db_name} не выгружена")

    delete_old_backups()


def sync_yadisk() -> None:
    """Выполнение синхронизации с Яндекс.Диск."""
    if not config.YANDEX_DISK_TOKEN:
        logger.error("Токен для сервиса Яндекс.Диск не задан!")
        return

    sync_new_files_to_yadisk()  # Синхронизация новых файлов
    sync_deleted_files_from_yadisk()  # Удаление файлов
    clear_yadisk_trash()
