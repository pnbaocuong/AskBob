"""
Add priority and due_date to task, plus helpful indexes

Revision ID: 0002_task_priority_due_date
Revises: 0001_initial
Create Date: 2025-08-20 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0002_task_priority_due_date'
down_revision: Union[str, None] = '0001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('task', sa.Column('priority', sa.String(length=20), nullable=False, server_default='medium'))
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))

    op.create_index('ix_task_status', 'task', ['status'])
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])


def downgrade() -> None:
    op.drop_index('ix_task_due_date', table_name='task')
    op.drop_index('ix_task_priority', table_name='task')
    op.drop_index('ix_task_status', table_name='task')

    op.drop_column('task', 'due_date')
    op.drop_column('task', 'priority')
