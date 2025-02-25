"""Тестирование конфигурации."""

import os
from unittest.mock import patch

import pytest
from backup_1c.configs.config import Config


@pytest.fixture
def env_vars():
    """Фикстура для базовых переменных окружения."""
    return {"DB_USER": "test_user", "DB_PASS": "test_pass"}


def test_config_init_defaults(env_vars):
    """Тест инициализации конфига с значениями по умолчанию."""
    # Arrange
    with patch.dict(os.environ, env_vars):
        # Act
        config = Config()
        # Assert
        assert config.LOG_PATH == "logs/app.log"
        assert config.TEMP_PATH == "tmp"
        assert config.DB_PATH == "app.sqlite3"
        assert config.DATABASE_URL == "sqlite:///app.sqlite3"
        assert config.BACKUP_FILE_LIFETIME == 90


@pytest.mark.parametrize(
    "env, error_msg",
    [
        (
            {"DB_USER": "", "DB_PASS": "pass"},
            "DB_USER или DB_PASS не установлены",
        ),
        (
            {"DB_USER": "user", "DB_PASS": ""},
            "DB_USER или DB_PASS не установлены",
        ),
        ({}, "DB_USER или DB_PASS не установлены"),
    ],
)
def test_config_init_missing_credentials(env, error_msg):
    """Тест ошибки при отсутствии учетных данных."""
    # Arrange
    with patch.dict(os.environ, env, clear=True):
        # Act & Assert
        with pytest.raises(ValueError, match=error_msg):
            Config()
