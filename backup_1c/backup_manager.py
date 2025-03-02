"""Управление созданием резервных копий 1С."""

import logging
from typing import List, Tuple

from backup_1c.configs.database import FileStatus
from backup_1c.models import DatabaseCreds, File
from backup_1c.utils import run_ibcmd

logger = logging.getLogger(__name__)


class BackupManager:
    """Менеджер для создания резервных копий 1С."""

    def __init__(self, db_manager):
        """Инициализация менеджера."""
        self.db_manager = db_manager

    def create_backups(self) -> Tuple[List[File], List[str]]:
        """Создаёт резервные копии для всех баз данных."""
        creds_list: List[DatabaseCreds] = (
            self.db_manager.get_all_database_creds()
        )
        created_files: List[File] = []
        failed_backups: List[str] = []

        for creds in creds_list:
            logger.info(f"Выгрузка базы {creds.db_name}")
            full_path = run_ibcmd(
                creds.db_name, creds.username, creds.password
            )
            if full_path:
                file = self.db_manager.get_file_by_path(full_path)
                if file:
                    self.db_manager.update_file_status(file.id, FileStatus.NEW)
                else:
                    file = self.db_manager.add_file(full_path)
                created_files.append(file)
                logger.info(f"Выгрузка базы {creds.db_name} завершена")
            else:
                failed_backups.append(creds.db_name)
                logger.error(f"База {creds.db_name} не выгружена")

        self.db_manager.delete_old_backups()
        return created_files, failed_backups
