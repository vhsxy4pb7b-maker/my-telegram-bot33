"""修复时区默认值

将所有 server_default 从 now() 改为 timezone('utc', now())

Revision ID: 005
Revises: 004
Create Date: 2024-12-07 08:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """更新所有时间字段的默认值为 UTC"""
    
    # 注意：PostgreSQL 中，ALTER COLUMN 不能直接修改 server_default
    # 需要先删除旧的默认值，然后添加新的默认值
    
    # customers 表
    try:
        op.execute("""
            ALTER TABLE customers 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass  # 如果已经更新过，忽略错误
    
    try:
        op.execute("""
            ALTER TABLE customers 
            ALTER COLUMN updated_at DROP DEFAULT
        """)
    except Exception:
        pass
    
    # conversations 表
    try:
        op.execute("""
            ALTER TABLE conversations 
            ALTER COLUMN received_at DROP DEFAULT,
            ALTER COLUMN received_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE conversations 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE conversations 
            ALTER COLUMN updated_at DROP DEFAULT
        """)
    except Exception:
        pass
    
    # collected_data 表
    try:
        op.execute("""
            ALTER TABLE collected_data 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE collected_data 
            ALTER COLUMN updated_at DROP DEFAULT
        """)
    except Exception:
        pass
    
    # reviews 表
    try:
        op.execute("""
            ALTER TABLE reviews 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE reviews 
            ALTER COLUMN updated_at DROP DEFAULT
        """)
    except Exception:
        pass
    
    # integration_logs 表
    try:
        op.execute("""
            ALTER TABLE integration_logs 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    # daily_statistics 表
    try:
        op.execute("""
            ALTER TABLE daily_statistics 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE daily_statistics 
            ALTER COLUMN updated_at DROP DEFAULT
        """)
    except Exception:
        pass
    
    # customer_interactions 表
    try:
        op.execute("""
            ALTER TABLE customer_interactions 
            ALTER COLUMN interaction_time DROP DEFAULT,
            ALTER COLUMN interaction_time SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE customer_interactions 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    # frequent_questions 表
    try:
        op.execute("""
            ALTER TABLE frequent_questions 
            ALTER COLUMN first_seen DROP DEFAULT,
            ALTER COLUMN first_seen SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE frequent_questions 
            ALTER COLUMN last_seen DROP DEFAULT,
            ALTER COLUMN last_seen SET DEFAULT timezone('utc', now())
        """)
    except Exception:
        pass


def downgrade() -> None:
    """回滚到使用 now() 作为默认值"""
    
    # customers 表
    try:
        op.execute("""
            ALTER TABLE customers 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # conversations 表
    try:
        op.execute("""
            ALTER TABLE conversations 
            ALTER COLUMN received_at DROP DEFAULT,
            ALTER COLUMN received_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE conversations 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # collected_data 表
    try:
        op.execute("""
            ALTER TABLE collected_data 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # reviews 表
    try:
        op.execute("""
            ALTER TABLE reviews 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # integration_logs 表
    try:
        op.execute("""
            ALTER TABLE integration_logs 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # daily_statistics 表
    try:
        op.execute("""
            ALTER TABLE daily_statistics 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # customer_interactions 表
    try:
        op.execute("""
            ALTER TABLE customer_interactions 
            ALTER COLUMN interaction_time DROP DEFAULT,
            ALTER COLUMN interaction_time SET DEFAULT now()
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE customer_interactions 
            ALTER COLUMN created_at DROP DEFAULT,
            ALTER COLUMN created_at SET DEFAULT now()
        """)
    except Exception:
        pass
    
    # frequent_questions 表
    try:
        op.execute("""
            ALTER TABLE frequent_questions 
            ALTER COLUMN first_seen DROP DEFAULT,
            ALTER COLUMN first_seen SET DEFAULT now()
        """)
    except Exception:
        pass
    
    try:
        op.execute("""
            ALTER TABLE frequent_questions 
            ALTER COLUMN last_seen DROP DEFAULT,
            ALTER COLUMN last_seen SET DEFAULT now()
        """)
    except Exception:
        pass

