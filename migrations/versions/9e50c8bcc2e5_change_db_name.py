"""change db_name

Revision ID: 9e50c8bcc2e5
Revises: 2dfbd76f140d
Create Date: 2025-02-24 21:04:25.054994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e50c8bcc2e5'
down_revision: Union[str, None] = '2dfbd76f140d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
