"""Точка входа программы."""

import logging

from backup_1c.config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

def initial() -> None:
    """Инициализация программы."""
    logger.info("Начало работы.")


if __name__ == "__main__":
    initial()
