"""Add is_deleted to File

Revision ID: 16928e83ca53
Revises: 9e50c8bcc2e5
Create Date: 2025-02-25 09:48:55.358745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16928e83ca53'
down_revision: Union[str, None] = '9e50c8bcc2e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_database_creds_db_name'), 'database_creds', ['db_name'], unique=True)
    op.add_column('files', sa.Column('is_deleted', sa.Boolean(), nullable=False))
    op.create_index(op.f('ix_files_date_added'), 'files', ['date_added'], unique=False)
    op.create_index(op.f('ix_files_is_deleted'), 'files', ['is_deleted'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_files_is_deleted'), table_name='files')
    op.drop_index(op.f('ix_files_date_added'), table_name='files')
    op.drop_column('files', 'is_deleted')
    op.drop_index(op.f('ix_database_creds_db_name'), table_name='database_creds')
    # ### end Alembic commands ###
