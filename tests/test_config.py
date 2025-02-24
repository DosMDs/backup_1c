"""Тестирование config.py."""

import os
from unittest.mock import patch

import pytest

from backup_1c.config.config import Config


@patch.dict(os.environ, {"DB_USER": "test_user", "DB_PASS": "test_pass"})
def test_config_init() -> None:
    """Тест инициализации класса Config."""
    config = Config()
    assert config.LOG_PATH == "logs/app.log"
    assert config.TEMP_PATH == "tmp"
    assert config.DB_PATH == "app.sqlite3"
    assert config.DATABASE_URL == "sqlite:///app.sqlite3"
    assert config.BACKUP_PATH == "/backup"
    assert config.ENTERPRISE_PATH == "/opt/1cv8/x86_64/"
    assert config.ENTERPRISE_VERSION is None
    assert config.DB_SERVER == "localhost"
    assert config.DBMS == "PostgreSQL"
    assert config.DB_USER == "test_user"
    assert config.DB_PASS == "test_pass"


@patch.dict(os.environ, {"DB_USER": "", "DB_PASS": ""})
def test_config_init_without_db_user_and_db_pass() -> None:
    """Тест инициализации класса Config без DB_USER и DB_PASS."""
    with pytest.raises(ValueError) as excinfo:
        Config()
    assert str(excinfo.value) == "DB_USER или DB_PASS не установлены"
