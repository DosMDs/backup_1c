"""Методы общего назначения."""

import logging
import subprocess
from datetime import datetime
from pathlib import Path

from backup_1c.config.config import config

logger = logging.getLogger(__name__)


def ensure_path_exists(file_path: str) -> str:
    """Проверяет и создает директорию для файла с помощью pathlib."""
    path = Path(file_path)
    directory = path.parent

    if not directory.exists():
        directory.mkdir(parents=True, mode=0o755)
        logger.info(f"Создана директория: {directory}")
    else:
        logger.info(f"Директория уже существует: {directory}")

    return str(path)


def run_ibcmd(db_name, user, password):
    """Выполняет команду ibcmd для создания резервной копии базы данных."""
    dt = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{db_name}_{dt}.dt"
    f_path = Path(config.BACKUP_PATH, db_name, file_name)

    logger.debug(f"db_name: {db_name}, user: {user}, pass: {password}",
                 f"f_path: {f_path}")

    backup_dir = f_path.parent
    if not backup_dir.exists():
        ensure_path_exists(backup_dir)

    temp_path = Path(config.TEMP_PATH)
    if not temp_path.exists():
        ensure_path_exists(temp_path)

    cmd = [
        f"/opt/1cv8/x86_64/{config['version_1c']}/ibcmd",
        "infobase",
        "dump",
        f"--db-server={config.DB_SERVER}",
        f"--dbms={config.DBMS}",
        f"--db-name={db_name}",
        f"--db-user={config.DB_USER}",
        f"--db-pwd={config.DB_PASS}",
        f"--data={temp_path}",
        f"--user={user}",
        f"--password={password}",
        str(f_path),
    ]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        error_message = result.stderr.decode("utf-8").strip()
        logger.error(
            f"Ошибка при выгрузке базы {db_name}:",
            f" код возврата {result.returncode}",
        )
        logger.error(f"Сообщение об ошибке: {error_message}")
