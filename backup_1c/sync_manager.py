"""Управление синхронизацией с облачным хранилищем."""

import logging
from typing import List

from backup_1c.configs.config import config
from backup_1c.configs.database import FileStatus
from backup_1c.models import File
from backup_1c.cloud_storage import CloudStorage
from backup_1c.telegram_utils import notify_telegram_sync

logger = logging.getLogger(__name__)


class SyncManager:
    """Менеджер для синхронизации файлов с облачным хранилищем."""

    def __init__(self, db_manager, cloud_storage: CloudStorage):
        self.db_manager = db_manager
        self.cloud_storage = cloud_storage

    def sync(
        self, created_files: List[File], failed_backups: List[str]
    ) -> None:
        """Выполняет полную синхронизацию с облаком."""
        if not config.YANDEX_DISK_TOKEN:
            logger.error("Токен для сервиса Яндекс.Диск не задан!")
            return

        synced_files = self._sync_new_files()
        self._sync_deleted_files()
        self.cloud_storage.clear_trash()

        if synced_files or failed_backups:
            notify_telegram_sync(synced_files, failed_backups)

    def _sync_new_files(self) -> List[File]:
        """Синхронизирует новые файлы с облаком."""
        new_files = self.db_manager.get_files_by_status(
            FileStatus.NEW, exclude_deleted=True
        )
        synced_files: List[File] = []

        for file in new_files:
            self.db_manager.update_file_status(file.id, FileStatus.SYNCING)
            download_link = self.cloud_storage.upload_file(file.full_path)
            if download_link:
                self.db_manager.update_file(
                    file.id,
                    status=FileStatus.PROCESSED,
                    download_link=download_link,
                )
                synced_files.append(file)
            else:
                self.db_manager.update_file_status(file.id, FileStatus.NEW)

        return synced_files

    def _sync_deleted_files(self) -> List[File]:
        """Синхронизирует удалённые файлы с облаком."""
        deleting_files = self.db_manager.get_files_by_status(
            FileStatus.DELETING, exclude_deleted=False
        )
        synced_files: List[File] = []

        for file in deleting_files:
            self.db_manager.update_file_status(file.id, FileStatus.SYNCING)
            if self.cloud_storage.delete_file(file.full_path):
                self.db_manager.update_file(
                    file.id, status=FileStatus.DELETED, download_link=None
                )
                synced_files.append(file)
            else:
                self.db_manager.update_file_status(
                    file.id, FileStatus.DELETING
                )

        return synced_files
