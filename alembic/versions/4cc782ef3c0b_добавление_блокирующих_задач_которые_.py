"""Добавление блокирующих задач которые могут быть нулями

Revision ID: 4cc782ef3c0b
Revises: eaf31ed56b90
Create Date: 2024-01-28 07:11:42.502523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cc782ef3c0b'
down_revision: Union[str, None] = 'eaf31ed56b90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'blocked_by_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'blocked_by_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
