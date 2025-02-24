"""ORM модели для сущностей БД."""

from sqlalchemy import Column, Integer, String

from backup_1c.config.database import Base


class DatabaseCreds(Base):
    """Модель для хранения информация по обрабатываемым базам данных."""

    __tablename__ = "database_creds"  # Имя таблицы в SQLite

    id = Column(
        Integer, primary_key=True, index=True
    )  # Уникальный идентификатор
    db_name = Column(String, nullable=False)  # Имя базы данных
    username = Column(String, nullable=False)  # Имя пользователя
    password = Column(String, nullable=False)  # Пароль

    def __repr__(self):
        """Текстовое представление."""
        return f"<DatabaseCreds(db_name='{self.db_name}')>"
