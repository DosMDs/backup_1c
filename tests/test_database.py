"""Тестирование файла database.py."""

from unittest.mock import Mock, patch

import pytest
from backup_1c.config.database import get_db
from sqlalchemy.orm import Session


@patch("backup_1c.config.database.SessionLocal", autospec=True)
def test_get_db(mock_session_local):
    """Тест генератора сессий для работы с базой."""
    mock_session = Mock(spec=Session)
    mock_session_local.return_value = mock_session

    db_generator = get_db()
    db = next(db_generator)

    assert db == mock_session
    mock_session.close.assert_not_called()

    with pytest.raises(StopIteration):
        next(db_generator)

    mock_session.close.assert_called_once()
