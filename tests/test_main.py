"""Тестирования точки входа в приложение."""

from unittest.mock import patch

from backup_1c.main import initial


def test_initial() -> None:
    """Тестирование инициации."""
    with patch("logging.Logger.info") as mock_info:
        initial()
        mock_info.assert_called_once_with("Начало работы.")
