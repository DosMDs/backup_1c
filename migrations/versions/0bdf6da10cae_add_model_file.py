"""add model File

Revision ID: 0bdf6da10cae
Revises: de451c7b3b78
Create Date: 2025-02-24 15:55:45.682739

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0bdf6da10cae'
down_revision: Union[str, None] = 'de451c7b3b78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
