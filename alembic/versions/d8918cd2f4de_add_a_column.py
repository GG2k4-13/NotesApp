"""Add a column

Revision ID: d8918cd2f4de
Revises: 
Create Date: 2024-10-18 01:09:57.289258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8918cd2f4de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('notes', sa.Column('note_title', sa.String, index=True))


def downgrade() -> None:
    op.drop_column('notes', 'note_title')
