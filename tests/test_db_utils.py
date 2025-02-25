"""Тестирование методов db_utils."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from backup_1c.configs.config import config
from backup_1c.configs.database import FileStatus
from backup_1c.db_utils import (
    add_file,
    delete_old_backups,
    get_file_by_path,
    get_files_by_status,
    sync_deleted_files_from_yadisk,
    sync_new_files_to_yadisk,
    update_file_status,
)
from backup_1c.models import File


@pytest.fixture
def mock_db():
    """Фикстура для мока базы данных."""
    db = MagicMock()
    with patch("backup_1c.db_utils.get_db", return_value=iter([db])):
        yield db


@pytest.fixture
def mock_yadisk():
    """Фикстура для мока Яндекс.Диска."""
    with patch("backup_1c.db_utils.upload_file_to_yadisk") as mock_upload:
        with patch(
            "backup_1c.db_utils.delete_file_from_yadisk"
        ) as mock_delete:
            with patch("backup_1c.db_utils.empty_trash") as mock_trash:
                yield mock_upload, mock_delete, mock_trash


def test_add_file(mock_db):
    """Тест добавления нового файла."""
    # Act
    result = add_file("/path/to/file.dt")

    # Assert
    assert result.full_path == "/path/to/file.dt"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)


@pytest.mark.parametrize(
    "status",
    [FileStatus.NEW, FileStatus.PROCESSED, FileStatus.DELETED],
)
def test_update_file_status_success(mock_db, status):
    """Тест успешного обновления статуса файла."""
    # Arrange
    mock_file = File(id=1, status=FileStatus.NEW)
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_file
    )

    # Act
    update_file_status(1, status)

    # Assert
    assert mock_file.status == status
    mock_db.commit.assert_called_once()


def test_update_file_status_invalid(mock_db):
    """Тест ошибки при некорректном статусе."""
    # Act & Assert
    with pytest.raises(ValueError, match="Статус должен быть из FileStatus"):
        update_file_status(1, "invalid")


def test_get_file_by_path_found(mock_db):
    """Тест получения файла по пути, если он существует."""
    # Arrange
    mock_file = File(full_path="/path/to/file.dt")
    mock_db.query.return_value.filter.return_value.first.return_value = (
        mock_file
    )

    # Act
    result = get_file_by_path("/path/to/file.dt")

    # Assert
    assert result == mock_file


def test_get_file_by_path_not_found(mock_db):
    """Тест получения файла, если его нет."""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = get_file_by_path("/nonexistent.dt")

    # Assert
    assert result is None


def test_get_files_by_status(mock_db):
    """Тест получения списка файлов по статусу."""
    # Arrange
    mock_files = [
        File(id=1, status=FileStatus.NEW),
        File(id=2, status=FileStatus.NEW),
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = (
        mock_files
    )

    # Act
    result = get_files_by_status(FileStatus.NEW)

    # Assert
    assert result == mock_files


def test_delete_old_backups(mock_db):
    """Тест удаления старых бэкапов."""
    # Arrange
    old_date = datetime.now() - timedelta(days=config.BACKUP_FILE_LIFETIME + 1)
    mock_file = File(
        full_path="old_file.dt", is_deleted=False, date_added=old_date
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    with patch("backup_1c.db_utils.calculate_threshold_date") as mock_calc:
        with patch("backup_1c.db_utils.delete_file", return_value=True):
            mock_calc.return_value = datetime.now() - timedelta(
                days=config.BACKUP_FILE_LIFETIME
            )

            # Act
            delete_old_backups()

            # Assert
            assert mock_file.status == FileStatus.DELETED
            assert mock_file.is_deleted
            mock_db.commit.assert_called_once()


def test_sync_new_files_to_yadisk_success(mock_db, mock_yadisk):
    """Тест успешной синхронизации новых файлов."""
    # Arrange
    mock_file = File(
        full_path="new_file.dt", status=FileStatus.NEW, is_deleted=False
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    mock_upload, _, _ = mock_yadisk
    mock_upload.return_value = "http://yandex.disk/link"

    # Act
    sync_new_files_to_yadisk()

    # Assert
    assert mock_file.status == FileStatus.PROCESSED
    assert mock_file.download_link == "http://yandex.disk/link"
    mock_db.commit.assert_called()


def test_sync_new_files_to_yadisk_failure(mock_db, mock_yadisk):
    """Тест неудачной синхронизации новых файлов."""
    # Arrange
    mock_file = File(
        full_path="new_file.dt", status=FileStatus.NEW, is_deleted=False
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    mock_upload, _, _ = mock_yadisk
    mock_upload.return_value = None

    # Act
    sync_new_files_to_yadisk()

    # Assert
    assert mock_file.status == FileStatus.NEW
    assert mock_file.download_link is None


def test_sync_deleted_files_from_yadisk_success(mock_db, mock_yadisk):
    """Тест успешного удаления файлов с Яндекс.Диска."""
    # Arrange
    mock_file = File(
        full_path="del_file.dt", status=FileStatus.DELETING, is_deleted=True
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    _, mock_delete, _ = mock_yadisk
    mock_delete.return_value = True

    # Act
    sync_deleted_files_from_yadisk()

    # Assert
    assert mock_file.status == FileStatus.DELETED
    assert mock_file.download_link is None


def test_sync_deleted_files_from_yadisk_failure(mock_db, mock_yadisk):
    """Тест неудачного удаления файлов с Яндекс.Диска."""
    # Arrange
    mock_file = File(
        full_path="del_file.dt", status=FileStatus.DELETING, is_deleted=True
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    _, mock_delete, _ = mock_yadisk
    mock_delete.return_value = False

    # Act
    sync_deleted_files_from_yadisk()

    # Assert
    assert mock_file.status == FileStatus.DELETING


def test_sync_new_files_to_yadisk_with_nested_path(mock_db, mock_yadisk):
    """Тест синхронизации файла с вложенной структурой каталогов."""
    # Arrange
    mock_file = File(
        full_path="/backup/retail/retail_2025-02-24.dt",
        status=FileStatus.NEW,
        is_deleted=False,
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_file
    ]
    mock_upload, _, _ = mock_yadisk
    mock_upload.return_value = "http://yandex.disk/link"

    # Act
    sync_new_files_to_yadisk()

    # Assert
    assert mock_file.status == FileStatus.PROCESSED
    assert mock_file.download_link == "http://yandex.disk/link"
    mock_upload.assert_called_once_with("/backup/retail/retail_2025-02-24.dt")
