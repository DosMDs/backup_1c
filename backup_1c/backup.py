"""Основная функциональность по выгрузке баз."""

import logging

from backup_1c.db_utils import get_all_database_creds, run_ibcmd

logger = logging.getLogger(__name__)


def backup_1c():
    """Выгрузка баз 1С через ibcmd."""
    creds_list = get_all_database_creds()
    for creds in creds_list:
        logger.info(f'Выгрузка базы {creds.db_name}')
        run_ibcmd(creds.db_name, creds.username, creds.password)
        logger.info(f'Выгрузка базы {creds.db_name} завершена')
