"""Add download_link to File

Revision ID: fcf1ccbb8e9c
Revises: 16928e83ca53
Create Date: 2025-02-25 11:27:47.361690

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fcf1ccbb8e9c"
down_revision: Union[str, None] = "9e50c8bcc2e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "files", sa.Column("download_link", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("files", "download_link")
    # ### end Alembic commands ###
