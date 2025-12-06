"""Telegram Bot 命令处理器"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from src.database.models import Review, ReviewStatus, Conversation, Customer
from src.database.database import get_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CommandProcessor:
    """处理 Telegram Bot 的审核命令"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_command(
        self,
        command: str,
        reviewer: str
    ) -> Dict[str, Any]:
        """
        处理命令
        
        Args:
            command: 命令文本（如 /approve_123）
            reviewer: 审核人标识
        
        Returns:
            处理结果
        """
        command = command.strip()
        
        if command.startswith("/approve_"):
            conversation_id = self._extract_id(command, "/approve_")
            return self.approve_review(conversation_id, reviewer)
        
        elif command.startswith("/reject_"):
            conversation_id = self._extract_id(command, "/reject_")
            return self.reject_review(conversation_id, reviewer)
        
        elif command.startswith("/review_"):
            conversation_id = self._extract_id(command, "/review_")
            return self.get_review_details(conversation_id)
        
        else:
            return {
                "success": False,
                "message": "未知命令"
            }
    
    def approve_review(
        self,
        conversation_id: int,
        reviewer: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        通过审核
        
        Args:
            conversation_id: 对话 ID
            reviewer: 审核人
            notes: 备注
        
        Returns:
            处理结果
        """
        try:
            conversation = self.db.query(Conversation)\
                .filter(Conversation.id == conversation_id)\
                .first()
            
            if not conversation:
                return {
                    "success": False,
                    "message": f"对话 {conversation_id} 不存在"
                }
            
            # 创建或更新审核记录
            review = self.db.query(Review)\
                .filter(Review.conversation_id == conversation_id)\
                .first()
            
            if not review:
                review = Review(
                    customer_id=conversation.customer_id,
                    conversation_id=conversation_id,
                    status=ReviewStatus.APPROVED,
                    reviewed_by=reviewer,
                    review_notes=notes,
                    reviewed_at=datetime.utcnow()
                )
                self.db.add(review)
            else:
                review.status = ReviewStatus.APPROVED
                review.reviewed_by = reviewer
                review.review_notes = notes
                review.reviewed_at = datetime.utcnow()
            
            # 标记对话为已处理
            conversation.is_processed = True
            
            self.db.commit()
            
            logger.info(f"Review approved for conversation {conversation_id} by {reviewer}")
            
            return {
                "success": True,
                "message": f"对话 {conversation_id} 已通过审核",
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error approving review: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"处理失败: {str(e)}"
            }
    
    def reject_review(
        self,
        conversation_id: int,
        reviewer: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        拒绝审核
        
        Args:
            conversation_id: 对话 ID
            reviewer: 审核人
            notes: 备注
        
        Returns:
            处理结果
        """
        try:
            conversation = self.db.query(Conversation)\
                .filter(Conversation.id == conversation_id)\
                .first()
            
            if not conversation:
                return {
                    "success": False,
                    "message": f"对话 {conversation_id} 不存在"
                }
            
            # 创建或更新审核记录
            review = self.db.query(Review)\
                .filter(Review.conversation_id == conversation_id)\
                .first()
            
            if not review:
                review = Review(
                    customer_id=conversation.customer_id,
                    conversation_id=conversation_id,
                    status=ReviewStatus.REJECTED,
                    reviewed_by=reviewer,
                    review_notes=notes,
                    reviewed_at=datetime.utcnow()
                )
                self.db.add(review)
            else:
                review.status = ReviewStatus.REJECTED
                review.reviewed_by = reviewer
                review.review_notes = notes
                review.reviewed_at = datetime.utcnow()
            
            # 标记对话为已处理
            conversation.is_processed = True
            
            self.db.commit()
            
            logger.info(f"Review rejected for conversation {conversation_id} by {reviewer}")
            
            return {
                "success": True,
                "message": f"对话 {conversation_id} 已拒绝",
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error rejecting review: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"处理失败: {str(e)}"
            }
    
    def get_review_details(self, conversation_id: int) -> Dict[str, Any]:
        """
        获取审核详情
        
        Args:
            conversation_id: 对话 ID
        
        Returns:
            详情信息
        """
        conversation = self.db.query(Conversation)\
            .filter(Conversation.id == conversation_id)\
            .first()
        
        if not conversation:
            return {
                "success": False,
                "message": f"对话 {conversation_id} 不存在"
            }
        
        customer = self.db.query(Customer)\
            .filter(Customer.id == conversation.customer_id)\
            .first()
        
        review = self.db.query(Review)\
            .filter(Review.conversation_id == conversation_id)\
            .first()
        
        return {
            "success": True,
            "conversation": {
                "id": conversation.id,
                "content": conversation.content,
                "message_type": conversation.message_type.value,
                "priority": conversation.priority.value,
                "created_at": conversation.created_at.isoformat() if conversation.created_at else None
            },
            "customer": {
                "id": customer.id if customer else None,
                "name": customer.name if customer else None,
                "email": customer.email if customer else None,
                "phone": customer.phone if customer else None
            },
            "review": {
                "status": review.status.value if review else "pending",
                "reviewed_by": review.reviewed_by if review else None,
                "review_notes": review.review_notes if review else None
            }
        }
    
    def _extract_id(self, command: str, prefix: str) -> Optional[int]:
        """从命令中提取 ID"""
        try:
            id_str = command.replace(prefix, "").strip()
            return int(id_str)
        except ValueError:
            return None


