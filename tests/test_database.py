"""Тестирование работы с базой данных."""

from unittest.mock import Mock, patch

import pytest
from backup_1c.configs.database import get_db
from sqlalchemy.orm import Session


@pytest.fixture
def mock_session():
    """Фикстура для мока сессии SQLAlchemy."""
    with patch(
        "backup_1c.configs.database.SessionLocal"
    ) as mock_session_local:
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        yield mock_session


def test_get_db_yields_session(mock_session):
    """Тест генерации сессии."""
    # Act
    db_gen = get_db()
    db = next(db_gen)

    # Assert
    assert db == mock_session
    mock_session.close.assert_not_called()


def test_get_db_closes_session(mock_session):
    """Тест закрытия сессии после использования."""
    # Act
    db_gen = get_db()
    next(db_gen)
    with pytest.raises(StopIteration):
        next(db_gen)

    # Assert
    mock_session.close.assert_called_once()
