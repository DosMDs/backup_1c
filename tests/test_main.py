"""Тестирования точки входа в приложение."""

from backup_1c.main import init


def test_init() -> None:
    """Тестирование инициации."""
    assert init() is None
