"""Тестирование методов utils."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from backup_1c.utils import ensure_path_exists, run_ibcmd


def test_ensure_path_exists_creates_dir() -> None:
    """Тест проверяет `ensure_path_exists`."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "new_dir" / "file.txt"
        result = ensure_path_exists(str(path))
        assert Path(result).parent.exists()
        assert result == str(path)


@patch("backup_1c.utils.subprocess.run")
@patch("backup_1c.utils.get_latest_enterprise_version")
@patch("backup_1c.utils.config")
def test_run_ibcmd_success(mock_config, mock_get_version, mock_subprocess):
    """Тест проверяет `run_ibcmd`."""
    mock_subprocess.return_value.returncode = 0
    mock_get_version.return_value = "8.3.20"
    mock_config.BACKUP_PATH = "backup"
    mock_config.ENTERPRISE_PATH = "/opt/1cv8/x86_64/"
    mock_config.ENTERPRISE_VERSION = None
    mock_config.DB_SERVER = "localhost"
    mock_config.DBMS = "PostgreSQL"
    mock_config.DB_USER = "db_user"
    mock_config.DB_PASS = "db_pass"

    result = run_ibcmd("test_db", "user", "pass")
    assert result.endswith(".dt")
    assert "test_db" in result
