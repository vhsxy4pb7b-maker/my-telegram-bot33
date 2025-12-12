"""数据库模型定义"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
import enum
from src.database.database import Base


class MessageType(str, enum.Enum):
    """消息类型枚举"""
    AD = "ad"  # 广告
    MESSAGE = "message"  # 私信
    COMMENT = "comment"  # 评论


class ReviewStatus(str, enum.Enum):
    """审核状态枚举"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    PROCESSING = "processing"  # 处理中


class Priority(str, enum.Enum):
    """优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Platform(str, enum.Enum):
    """平台枚举"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    WHATSAPP = "whatsapp"


class Customer(Base):
    """客户信息表"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    # 平台相关字段
    platform = Column(Enum(Platform), default=Platform.FACEBOOK,
                      nullable=False, index=True)
    platform_user_id = Column(String(100), index=True)  # 通用平台用户ID
    platform_metadata = Column(JSON)  # 平台特定数据（JSON格式）

    # 兼容字段（保留用于向后兼容）
    facebook_id = Column(String(100), index=True)

    # 客户信息
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    company_name = Column(String(200))
    location = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    conversations = relationship("Conversation", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")


class Conversation(Base):
    """对话记录表"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # 平台相关字段
    platform = Column(Enum(Platform), default=Platform.FACEBOOK,
                      nullable=False, index=True)
    platform_message_id = Column(String(200), index=True)  # 通用平台消息ID

    # 兼容字段（保留用于向后兼容）
    facebook_message_id = Column(String(200), index=True)

    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    raw_data = Column(JSON)  # 原始平台数据

    # AI 回复相关
    ai_replied = Column(Boolean, default=False)
    ai_reply_content = Column(Text)
    ai_reply_at = Column(DateTime(timezone=True))

    # 状态
    is_processed = Column(Boolean, default=False)
    priority = Column(Enum(Priority), default=Priority.LOW)
    filtered = Column(Boolean, default=False)
    filter_reason = Column(String(500))

    # 时间戳
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    customer = relationship("Customer", back_populates="conversations")
    reviews = relationship("Review", back_populates="conversation")
    collected_data = relationship(
        "CollectedData", back_populates="conversation")


class CollectedData(Base):
    """收集的资料表"""
    __tablename__ = "collected_data"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey(
        "conversations.id"), nullable=False)

    # 收集的字段（JSON 格式存储）
    data = Column(JSON, nullable=False)

    # 验证状态
    is_validated = Column(Boolean, default=False)
    validation_errors = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    conversation = relationship(
        "Conversation", back_populates="collected_data")


class Review(Base):
    """审核记录表"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey(
        "conversations.id"), nullable=False)

    # 审核信息
    status = Column(Enum(ReviewStatus),
                    default=ReviewStatus.PENDING, nullable=False)
    reviewed_by = Column(String(100))  # 审核人（Telegram username 或 AI）
    review_notes = Column(Text)
    ai_assistance = Column(Boolean, default=False)  # 是否使用 AI 辅助
    ai_suggestion = Column(Text)  # AI 建议

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    customer = relationship("Customer", back_populates="reviews")
    conversation = relationship("Conversation", back_populates="reviews")


class IntegrationLog(Base):
    """集成日志表（ManyChat/Botcake）"""
    __tablename__ = "integration_logs"

    id = Column(Integer, primary_key=True, index=True)
    integration_type = Column(String(50), nullable=False)  # manychat, botcake
    action = Column(String(100), nullable=False)  # sync, send, receive
    status = Column(String(50), nullable=False)  # success, failed
    request_data = Column(JSON)
    response_data = Column(JSON)
    error_message = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
