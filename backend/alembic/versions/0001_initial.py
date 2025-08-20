"""
Initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-19 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tenant',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False, unique=True),
        sa.Column('domain', sa.String(length=255), nullable=True, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'user',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_user_email', 'user', ['email'])
    op.create_index('ix_user_tenant', 'user', ['tenant_id'])

    op.create_table(
        'project',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_project_tenant', 'project', ['tenant_id'])

    op.create_table(
        'task',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='todo'),
        sa.Column('assignee', sa.String(length=255), nullable=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('project.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_task_project_tenant', 'task', ['project_id', 'tenant_id'])
    op.create_index('ix_task_tenant', 'task', ['tenant_id'])


def downgrade() -> None:
    op.drop_index('ix_task_tenant', table_name='task')
    op.drop_index('ix_task_project_tenant', table_name='task')
    op.drop_table('task')

    op.drop_index('ix_project_tenant', table_name='project')
    op.drop_table('project')

    op.drop_index('ix_user_tenant', table_name='user')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')

    op.drop_table('tenant')
