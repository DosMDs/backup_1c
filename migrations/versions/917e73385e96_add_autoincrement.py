"""add autoincrement

Revision ID: 917e73385e96
Revises: 180512ae7fdd
Create Date: 2025-02-24 16:32:34.358801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '917e73385e96'
down_revision: Union[str, None] = '180512ae7fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
