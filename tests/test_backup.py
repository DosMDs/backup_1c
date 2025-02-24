"""Тестирование файла backup.py."""

from unittest.mock import patch

from backup_1c.backup import backup_1c
from backup_1c.models import DatabaseCreds


@patch("backup_1c.backup.get_all_database_creds", autospec=True)
@patch("backup_1c.backup.run_ibcmd", autospec=True)
@patch("backup_1c.backup.add_file", autospec=True)
def test_backup_1c(mock_add_file, mock_run_ibcmd, mock_get_all_database_creds):
    """Тест функции backup_1c."""
    mock_creds_list = [
        DatabaseCreds(db_name="db1", username="user1", password="pass1"),
        DatabaseCreds(db_name="db2", username="user2", password="pass2"),
    ]
    mock_get_all_database_creds.return_value = mock_creds_list

    mock_run_ibcmd.side_effect = ["path1", None]

    backup_1c()

    mock_get_all_database_creds.assert_called_once()
    assert mock_run_ibcmd.call_args_list == [
        (("db1", "user1", "pass1"), {}),
        (("db2", "user2", "pass2"), {}),
    ]
    mock_add_file.assert_called_once_with("path1")
