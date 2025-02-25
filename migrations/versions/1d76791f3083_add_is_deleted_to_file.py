"""Add is_deleted to File

Revision ID: 1d76791f3083
Revises: fcf1ccbb8e9c
Create Date: 2025-02-25 13:56:03.093416

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1d76791f3083"
down_revision: Union[str, None] = "fcf1ccbb8e9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "files",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, default=False),
    )
    op.create_index(
        op.f("ix_files_date_added"), "files", ["date_added"], unique=False
    )
    op.create_index(
        op.f("ix_files_is_deleted"), "files", ["is_deleted"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_files_is_deleted"), table_name="files")
    op.drop_index(op.f("ix_files_date_added"), table_name="files")
    op.drop_column("files", "is_deleted")
