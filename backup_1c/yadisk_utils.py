"""Утилиты для работы с Яндекс.Диском."""

import logging
from pathlib import Path
from typing import Optional

import yadisk

from backup_1c.configs.config import config

logger = logging.getLogger(__name__)

yandex_disk = yadisk.YaDisk(token=config.YANDEX_DISK_TOKEN)


def create_remote_directories(
    yandex_disk: yadisk.YaDisk, remote_path: str
) -> None:
    """Рекурсивно создаёт структуру каталогов на Яндекс.Диске."""
    if not remote_path or yandex_disk.exists(remote_path):
        return

    parent_path = str(Path(remote_path).parent)
    if parent_path != remote_path:
        create_remote_directories(yandex_disk, parent_path)

    try:
        yandex_disk.mkdir(remote_path)
        logger.debug(f"Создана директория на Яндекс.Диске: {remote_path}")
    except Exception as e:
        logger.error(f"Ошибка создания директории {remote_path}: {e}")
        raise


def upload_file_to_yadisk(local_path: str) -> Optional[str]:
    """Загружает файл на Яндекс.Диск, и возвращает ссылку на скачивание."""
    local_path_obj = Path(local_path)
    remote_base_path = "/backups"

    try:
        relative_path = local_path_obj.relative_to(Path(config.BACKUP_PATH))
        remote_path = f"{remote_base_path}/{relative_path}"

        remote_dir = str(Path(remote_path).parent)
        create_remote_directories(yandex_disk, remote_dir)

        yandex_disk.upload(local_path, remote_path, overwrite=True)
        link = yandex_disk.get_download_link(remote_path)
        logger.info(
            f"Файл {local_path} загружен на Яндекс.Диск, ссылка: {link}"
        )
        return link
    except Exception as e:
        logger.error(f"Ошибка загрузки {local_path} на Яндекс.Диск: {e}")
        return None


def delete_file_from_yadisk(remote_path: str) -> bool:
    """Удаляет файл с Яндекс.Диска."""
    try:
        yandex_disk.remove(
            remote_path, permanently=False
        )  # Помещаем в корзину
        logger.info(f"Файл {remote_path} удалён с Яндекс.Диска (в корзину)")
        return True
    except Exception as e:
        logger.error(f"Ошибка удаления {remote_path} с Яндекс.Диска: {e}")
        return False


def empty_trash() -> bool:
    """Очищает корзину на Яндекс.Диске."""
    try:
        yandex_disk.remove_trash("")
        logger.info("Корзина на Яндекс.Диске очищена")
        return True
    except Exception as e:
        logger.error(f"Ошибка очистки корзины на Яндекс.Диске: {e}")
        return False
