"""Роль сделал чтобы могло быть Null

Revision ID: 7e3e545bca8c
Revises: 4b7b59f4dd24
Create Date: 2024-01-24 15:27:28.764118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7e3e545bca8c'
down_revision: Union[str, None] = '4b7b59f4dd24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=postgresql.ENUM('meneger', 'developer', 'team_leader', 'test_engineer', name='role'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=postgresql.ENUM('meneger', 'developer', 'team_leader', 'test_engineer', name='role'),
               nullable=False)
    # ### end Alembic commands ###
