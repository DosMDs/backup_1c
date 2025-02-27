"""ORM модели для сущностей БД."""

import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backup_1c.configs.database import Base, FileStatus


class DatabaseCreds(Base):
    """Модель для хранения информация по обрабатываемым базам данных."""

    __tablename__ = "database_creds"  # Имя таблицы в SQLite

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    db_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        """Текстовое представление."""
        return f"<DatabaseCreds(db_name='{self.db_name}')>"


class File(Base):
    """Модель для хранения информации по выгруженным файлам."""

    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    full_path: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus), default=FileStatus.NEW, nullable=False, index=True
    )
    date_added: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
        nullable=False,
        index=True,
    )
    date_modified: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True
    )
    download_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        """Текстовое представление."""
        return f"<File(path='{self.full_path}', status='{self.status.value}')>"
