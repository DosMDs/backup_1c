"""Методы общего назначения."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_path_exists(file_path: str) -> str:
    """Проверяет и создает директорию для файла с помощью pathlib."""
    path = Path(file_path)
    directory = path.parent

    if not directory.exists():
        directory.mkdir(parents=True, mode=0o755)
        logger.info(f"Создана директория: {directory}")
    else:
        logger.info(f"Директория уже существует: {directory}")

    return str(path)
