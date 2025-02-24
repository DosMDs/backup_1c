"""update DatabaseCreds models

Revision ID: de451c7b3b78
Revises: dfe48478627f
Create Date: 2025-02-24 13:22:33.409964

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'de451c7b3b78'
down_revision: Union[str, None] = 'dfe48478627f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
