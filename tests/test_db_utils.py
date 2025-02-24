"""Тестирование методов db_utils."""

from unittest.mock import MagicMock

import pytest
from backup_1c.db_utils import add_file, update_file_status


def test_add_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирование добавления файла в базу."""
    db_mock = MagicMock()
    monkeypatch.setattr("backup_1c.db_utils.get_db", lambda: iter([db_mock]))
    result = add_file("/path/to/file.dt")
    assert result.full_path == "/path/to/file.dt"
    db_mock.commit.assert_called_once()


def test_update_file_status_invalid_type() -> None:
    """Тестирование изменения статуса файла."""
    with pytest.raises(ValueError, match="Статус должен быть из FileStatus"):
        update_file_status(1, "invalid_status")
