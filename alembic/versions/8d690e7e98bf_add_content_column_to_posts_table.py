"""add content column to posts table

Revision ID: 8d690e7e98bf
Revises: 968847d5eca0
Create Date: 2026-10-17 00:18:09.074007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d690e7e98bf'
down_revision: Union[str, Sequence[str], None] = '968847d5eca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
