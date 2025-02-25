"""Точка входа программы."""

import logging

from backup_1c.backup import backup_1c, sync_yadisk
from backup_1c.configs.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def initial() -> None:
    """Инициализация программы."""
    logger.info("Начало работы.")
    backup_1c()
    sync_yadisk()
    logger.info("Завершение работы.")


if __name__ == "__main__":
    initial()
