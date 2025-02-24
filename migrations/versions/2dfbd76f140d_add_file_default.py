"""add file default

Revision ID: 2dfbd76f140d
Revises: 917e73385e96
Create Date: 2025-02-24 18:02:28.093993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dfbd76f140d'
down_revision: Union[str, None] = '917e73385e96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
