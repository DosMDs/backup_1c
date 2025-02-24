"""Тестирование config.py."""

import os
from unittest.mock import patch

import pytest

from backup_1c.config.config import Config


@patch.dict(os.environ, {"DB_USER": "", "DB_PASS": ""})
def test_config_init_without_db_user_and_db_pass():
    """Тест инициализации класса Config без DB_USER и DB_PASS."""
    with pytest.raises(ValueError) as excinfo:
        Config()
    assert str(excinfo.value) == "DB_USER или DB_PASS не установлены"
