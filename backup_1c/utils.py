"""Методы общего назначения."""

import logging
import subprocess
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from backup_1c.configs.config import config

logger = logging.getLogger(__name__)


def ensure_path_exists(ensure_path: str, is_file: bool = True) -> str:
    """Проверяет и создает директорию с помощью pathlib."""
    path = Path(ensure_path)

    directory = path.parent if is_file else path
    if not directory.exists():
        directory.mkdir(parents=True, mode=0o755, exist_ok=True)
        logger.info(f"Создана директория: {directory}")

    return str(path)


@lru_cache(maxsize=1)
def get_latest_enterprise_version(enterprise_path: str) -> None | str:
    """Находит каталог с последней версией в указанной директории."""
    path = Path(enterprise_path)
    if not path.is_dir():
        logger.error(f"Путь к версиям 1С: {enterprise_path} не существует!")
        return None

    dirs = [dir for dir in path.iterdir() if dir.is_dir()]

    if not dirs:
        logger.error(f"В {path} нет каталогов.")
        return None

    version_dirs = []
    for dir in dirs:
        if all(part.isdigit() for part in dir.name.split(".")):
            version_dirs.append(dir)

    if not version_dirs:
        logger.error(f"В {path} нет каталогов с версиями.")
        return None

    latest_dir = max(
        version_dirs, key=lambda x: [int(part) for part in x.name.split(".")]
    )
    logger.debug(f"Последняя версия: {latest_dir.name} (путь: {latest_dir})")
    return latest_dir.name


def run_ibcmd(db_name: str, user: str, password: str) -> None | str:
    """Выполняет команду ibcmd для создания резервной копии базы данных."""
    dt = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{db_name}_{dt}.dt"
    f_path = Path(config.BACKUP_PATH, db_name, file_name)

    logger.debug(
        f"db_name: {db_name}, user: {user}, pass: {password}"
        f"f_path: {str(f_path)}"
    )

    ensure_path_exists(str(f_path))

    enterprise_version = config.ENTERPRISE_VERSION
    if not enterprise_version:
        enterprise_version = get_latest_enterprise_version(
            config.ENTERPRISE_PATH
        )
        if not enterprise_version:
            logger.error("Не удалось определить версию 1С для ibcmd")
            return None

    ibcmd_path = str(Path(config.ENTERPRISE_PATH, enterprise_version, "ibcmd"))
    cmd = [
        ibcmd_path,
        "infobase",
        "dump",
        f"--db-server={config.DB_SERVER}",
        f"--dbms={config.DBMS}",
        f"--db-name={db_name}",
        f"--db-user={config.DB_USER}",
        f"--db-pwd={config.DB_PASS}",
        f"--user={user}",
        f"--password={password}",
        str(f_path),
    ]

    logger.debug(cmd)

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        error_message = result.stderr.decode("utf-8").strip()
        logger_error_message = (
            f"Ошибка при выгрузке базы {db_name}:"
            f" код возврата {result.returncode}"
        )
        logger.error(logger_error_message)
        logger.error(f"Сообщение об ошибке: {error_message}")
        return None

    return str(f_path)
