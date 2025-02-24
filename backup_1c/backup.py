"""Основная функциональность по выгрузке баз."""

import logging
from typing import List

from backup_1c.db_utils import add_file, get_all_database_creds
from backup_1c.models import DatabaseCreds
from backup_1c.utils import run_ibcmd

logger = logging.getLogger(__name__)


def backup_1c() -> None:
    """Выгрузка баз 1С через ibcmd."""
    creds_list: List[DatabaseCreds] = get_all_database_creds()
    for creds in creds_list:
        logger.info(f"Выгрузка базы {creds.db_name}")
        full_path = run_ibcmd(creds.db_name, creds.username, creds.password)
        if full_path:
            add_file(full_path)
            logger.info(f"Выгрузка базы {creds.db_name} завершена")
        else:
            logger.error(f"База {creds.db_name} не выгружена")
