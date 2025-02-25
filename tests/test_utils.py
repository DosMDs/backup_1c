"""Тестирование утилит."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from backup_1c.utils import (
    ensure_path_exists,
    get_latest_enterprise_version,
    run_ibcmd,
)


@pytest.fixture
def temp_dir():
    """Фикстура для временной директории."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_ensure_path_exists(temp_dir):
    """Тест создания директории для файла."""
    # Arrange
    path = temp_dir / "new_dir" / "file.txt"

    # Act
    result = ensure_path_exists(str(path))

    # Assert
    assert path.parent.exists()
    assert result == str(path)


def test_get_latest_enterprise_version_success(temp_dir):
    """Тест поиска последней версии 1С."""
    # Arrange
    (temp_dir / "8.3.19").mkdir()
    (temp_dir / "8.3.20").mkdir()
    (temp_dir / "not_a_version").mkdir()

    # Act
    result = get_latest_enterprise_version(str(temp_dir))

    # Assert
    assert result == "8.3.20"


def test_get_latest_enterprise_version_no_versions(temp_dir):
    """Тест случая без версий."""
    # Act
    result = get_latest_enterprise_version(str(temp_dir))

    # Assert
    assert result is None


@pytest.fixture
def mock_config():
    """Фикстура для мока конфига."""
    with patch("backup_1c.utils.config") as mock:
        mock.BACKUP_PATH = "backup"
        mock.ENTERPRISE_PATH = "/opt/1cv8/x86_64/"
        mock.ENTERPRISE_VERSION = None
        mock.DB_SERVER = "localhost"
        mock.DBMS = "PostgreSQL"
        mock.DB_USER = "db_user"
        mock.DB_PASS = "db_pass"
        yield mock


def test_run_ibcmd_success(mock_config, temp_dir):
    """Тест успешного выполнения ibcmd."""
    # Arrange
    with patch(
        "backup_1c.utils.get_latest_enterprise_version", return_value="8.3.20"
    ):
        with patch("subprocess.run", return_value=Mock(returncode=0)):
            # Act
            result = run_ibcmd("test_db", "user", "pass")

            # Assert
            assert result.endswith(".dt")
            assert "test_db" in result


def test_run_ibcmd_failure(mock_config):
    """Тест ошибки при выполнении ibcmd."""
    # Arrange
    with patch(
        "backup_1c.utils.get_latest_enterprise_version", return_value="8.3.20"
    ):
        with patch(
            "subprocess.run", return_value=Mock(returncode=1, stderr=b"error")
        ):
            # Act
            result = run_ibcmd("test_db", "user", "pass")

            # Assert
            assert result is None
