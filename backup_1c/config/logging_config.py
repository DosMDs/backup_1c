"""Модуль базовой настройки логгера."""
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Настройка логгера."""
    # Основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень

    # Формат логов: время, уровень, имя модуля, сообщение
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # В консоль только INFO и выше
    console_handler.setFormatter(formatter)

    # Обработчик для файла с ротацией
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10000,  # Новый файл после 10 КБ
        backupCount=3    # Храним 3 старых файла
    )
    file_handler.setLevel(logging.DEBUG)  # В файл пишем всё от DEBUG
    file_handler.setFormatter(formatter)

    # Очищаем старые обработчики (если есть) и добавляем новые
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    setup_logging()
    logging.info("Логирование настроено!")
