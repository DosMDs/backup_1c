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
def test_run_ibcmd_success(mock_subprocess) -> None:
    """Тест проверяет `run_ibcmd`."""
    mock_subprocess.return_value.returncode = 0
    result = run_ibcmd("test_db", "user", "pass")
    assert result.endswith(".dt")
