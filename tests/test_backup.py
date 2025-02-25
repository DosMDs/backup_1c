"""Тестирование основной функции backup_1c."""

from unittest.mock import Mock, patch

import pytest
from backup_1c.backup import backup_1c
from backup_1c.configs.database import FileStatus
from backup_1c.models import DatabaseCreds


@pytest.fixture
def mock_db_creds():
    """Фикстура для списка учетных данных баз данных."""
    return [
        DatabaseCreds(db_name="db1", username="user1", password="pass1"),
        DatabaseCreds(db_name="db2", username="user2", password="pass2"),
    ]


@pytest.fixture
def mock_run_ibcmd():
    """Фикстура для мока run_ibcmd."""
    with patch("backup_1c.backup.run_ibcmd") as mock:
        yield mock


@pytest.fixture
def mock_add_file():
    """Фикстура для мока add_file."""
    with patch("backup_1c.backup.add_file") as mock:
        yield mock


@pytest.fixture
def mock_get_file_by_path():
    """Фикстура для мока get_file_by_path."""
    with patch("backup_1c.backup.get_file_by_path") as mock:
        yield mock


@pytest.fixture
def mock_update_file_status():
    """Фикстура для мока update_file_status."""
    with patch("backup_1c.backup.update_file_status") as mock:
        yield mock


def test_backup_1c_success(
    mock_db_creds,
    mock_run_ibcmd,
    mock_add_file,
    mock_get_file_by_path,
    mock_update_file_status,
):
    """Тест успешного создания бэкапов для всех баз."""
    # Arrange
    with patch(
        "backup_1c.backup.get_all_database_creds", return_value=mock_db_creds
    ):
        mock_run_ibcmd.side_effect = ["path/to/db1.dt", "path/to/db2.dt"]
        mock_get_file_by_path.return_value = None

        # Act
        backup_1c()

        # Assert
        assert mock_run_ibcmd.call_count == 2
        mock_run_ibcmd.assert_any_call("db1", "user1", "pass1")
        mock_run_ibcmd.assert_any_call("db2", "user2", "pass2")
        assert mock_add_file.call_count == 2
        mock_add_file.assert_any_call("path/to/db1.dt")
        mock_add_file.assert_any_call("path/to/db2.dt")
        mock_update_file_status.assert_not_called()


def test_backup_1c_existing_file(
    mock_db_creds,
    mock_run_ibcmd,
    mock_add_file,
    mock_get_file_by_path,
    mock_update_file_status,
):
    """Тест обновления статуса существующего файла."""
    # Arrange
    mock_file = Mock(id=1)
    with patch(
        "backup_1c.backup.get_all_database_creds",
        return_value=[mock_db_creds[0]],
    ):
        mock_run_ibcmd.return_value = "path/to/db1.dt"
        mock_get_file_by_path.return_value = mock_file

        # Act
        backup_1c()

        # Assert
        mock_add_file.assert_not_called()
        mock_update_file_status.assert_called_once_with(1, FileStatus.NEW)


def test_backup_1c_partial_failure(
    mock_db_creds,
    mock_run_ibcmd,
    mock_add_file,
    mock_get_file_by_path,
):
    """Тест частичного сбоя при создании бэкапов."""
    # Arrange
    with patch(
        "backup_1c.backup.get_all_database_creds", return_value=mock_db_creds
    ):
        mock_run_ibcmd.side_effect = ["path/to/db1.dt", None]
        mock_get_file_by_path.return_value = None

        # Act
        backup_1c()

        # Assert
        mock_add_file.assert_called_once_with("path/to/db1.dt")
        assert mock_run_ibcmd.call_count == 2
