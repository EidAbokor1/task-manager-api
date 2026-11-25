"""create tasks table

Revision ID: 4a716e969ec2
Revises:
Create Date: 2026-11-24 17:07:37.275227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a716e969ec2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
    sa.Column(
        "id", sa.Integer(), sa.Identity(always=True),
        primary_key=True,
    ),
    sa.Column("title", sa.Text(), nullable=False),
    sa.Column(
        "completed", sa.Boolean(),
        nullable=False, server_default=sa.false(),
    ),
)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
