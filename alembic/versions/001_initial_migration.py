"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 customers 表
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('facebook_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('company_name', sa.String(length=200), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_index(op.f('ix_customers_facebook_id'),
                    'customers', ['facebook_id'], unique=True)

    # 创建 conversations 表
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('facebook_message_id', sa.String(length=200), nullable=True),
        sa.Column('message_type', sa.Enum('ad', 'message',
                  'comment', name='messagetype'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('raw_data', postgresql.JSON(
            astext_type=sa.Text()), nullable=True),
        sa.Column('ai_replied', sa.Boolean(), nullable=True),
        sa.Column('ai_reply_content', sa.Text(), nullable=True),
        sa.Column('ai_reply_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=True),
        sa.Column('priority', sa.Enum('low', 'medium', 'high',
                  'urgent', name='priority'), nullable=True),
        sa.Column('filtered', sa.Boolean(), nullable=True),
        sa.Column('filter_reason', sa.String(length=500), nullable=True),
        sa.Column('received_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_id'),
                    'conversations', ['id'], unique=False)
    op.create_index(op.f('ix_conversations_facebook_message_id'),
                    'conversations', ['facebook_message_id'], unique=True)

    # 创建 collected_data 表
    op.create_table(
        'collected_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('data', postgresql.JSON(
            astext_type=sa.Text()), nullable=False),
        sa.Column('is_validated', sa.Boolean(), nullable=True),
        sa.Column('validation_errors', postgresql.JSON(
            astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collected_data_id'),
                    'collected_data', ['id'], unique=False)

    # 创建 reviews 表
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected',
                  'processing', name='reviewstatus'), nullable=False),
        sa.Column('reviewed_by', sa.String(length=100), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('ai_assistance', sa.Boolean(), nullable=True),
        sa.Column('ai_suggestion', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=False)

    # 创建 integration_logs 表
    op.create_table(
        'integration_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('integration_type', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('request_data', postgresql.JSON(
            astext_type=sa.Text()), nullable=True),
        sa.Column('response_data', postgresql.JSON(
            astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integration_logs_id'),
                    'integration_logs', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_integration_logs_id'),
                  table_name='integration_logs')
    op.drop_table('integration_logs')
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_collected_data_id'), table_name='collected_data')
    op.drop_table('collected_data')
    op.drop_index(op.f('ix_conversations_facebook_message_id'),
                  table_name='conversations')
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_customers_facebook_id'), table_name='customers')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_table('customers')

