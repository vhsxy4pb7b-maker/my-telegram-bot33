"""添加性能优化索引

Revision ID: 006_add_performance_indexes
Revises: 005_fix_timezone_defaults
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_add_performance_indexes'
down_revision = '005_fix_timezone_defaults'
branch_labels = None
depends_on = None


def upgrade():
    # 为Conversation表添加复合索引
    op.create_index(
        'idx_conversations_customer_status',
        'conversations',
        ['customer_id', 'status', 'received_at'],
        unique=False
    )
    
    op.create_index(
        'idx_conversations_platform_processed',
        'conversations',
        ['platform', 'is_processed', 'received_at'],
        unique=False
    )
    
    op.create_index(
        'idx_conversations_priority_status',
        'conversations',
        ['priority', 'status', 'received_at'],
        unique=False
    )
    
    # 为Customer表添加复合索引
    op.create_index(
        'idx_customers_platform_user',
        'customers',
        ['platform', 'platform_user_id'],
        unique=False
    )
    
    # 为CollectedData表添加索引
    op.create_index(
        'idx_collected_data_conversation_field',
        'collected_data',
        ['conversation_id', 'field_name'],
        unique=False
    )
    
    # 为Review表添加索引
    op.create_index(
        'idx_reviews_conversation_status',
        'reviews',
        ['conversation_id', 'status', 'created_at'],
        unique=False
    )


def downgrade():
    op.drop_index('idx_reviews_conversation_status', table_name='reviews')
    op.drop_index('idx_collected_data_conversation_field', table_name='collected_data')
    op.drop_index('idx_customers_platform_user', table_name='customers')
    op.drop_index('idx_conversations_priority_status', table_name='conversations')
    op.drop_index('idx_conversations_platform_processed', table_name='conversations')
    op.drop_index('idx_conversations_customer_status', table_name='conversations')

