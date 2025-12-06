"""数据库连接和会话管理"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.config import settings

# 创建数据库引擎
connect_args = {}
if "sqlite" in settings.database_url:
    # SQLite 需要特殊配置
    connect_args = {"check_same_thread": False}
    poolclass = NullPool
else:
    poolclass = None

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    poolclass=poolclass,
    pool_pre_ping=True if "sqlite" not in settings.database_url else False,
    connect_args=connect_args,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
