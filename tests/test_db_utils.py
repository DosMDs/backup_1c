"""Тестирование методов db_utils."""

from unittest.mock import MagicMock

from backup_1c.db_utils import add_file


def test_add_file(monkeypatch):
    """Тестирование добавления файла в базу."""
    db_mock = MagicMock()
    monkeypatch.setattr("backup_1c.db_utils.get_db", lambda: iter([db_mock]))
    result = add_file("/path/to/file.dt")
    assert result.full_path == "/path/to/file.dt"
    db_mock.commit.assert_called_once()
