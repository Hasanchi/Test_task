"""inital2

Revision ID: 919bfbbe6fb2
Revises: 70db0c6d5ac6
Create Date: 2024-01-23 08:59:36.619710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '919bfbbe6fb2'
down_revision: Union[str, None] = '70db0c6d5ac6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('meneger', 'developer', 'team_leader', 'test_engineer', name='role'), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('bug', 'task', name='type'), nullable=False),
    sa.Column('priority', sa.Enum('critical', 'high', 'medium', 'low', name='priority'), nullable=False),
    sa.Column('status', sa.Enum('to_do', 'in_progress', 'code_review', 'dev_test', 'testing', 'done', 'wontfix', name='status'), nullable=False),
    sa.Column('heading', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('executor_id', sa.Integer(), nullable=True),
    sa.Column('сreator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['executor_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['сreator_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_id'), 'task', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###