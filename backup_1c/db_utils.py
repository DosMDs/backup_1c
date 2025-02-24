"""Методы для работы с данными."""

from backup_1c.config.database import get_db
from backup_1c.models import DatabaseCreds


def get_all_database_creds():
    """Получает список всех баз данных из таблицы database_creds."""
    db = next(get_db())
    creds_list = db.query(DatabaseCreds).all()  # Запрашиваем все записи
    return creds_list
