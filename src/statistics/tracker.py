"""统计数据追踪器"""
from datetime import date, datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from src.database.statistics_models import DailyStatistics, CustomerInteraction, FrequentQuestion
import logging

logger = logging.getLogger(__name__)


class StatisticsTracker:
    """统计数据追踪器"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_daily_statistics(self, target_date: Optional[date] = None) -> DailyStatistics:
        """获取或创建每日统计数据"""
        if target_date is None:
            target_date = date.today()
        
        stats = self.db.query(DailyStatistics)\
            .filter(DailyStatistics.date == target_date)\
            .first()
        
        if not stats:
            stats = DailyStatistics(date=target_date)
            self.db.add(stats)
            self.db.commit()
            self.db.refresh(stats)
        
        return stats
    
    def record_customer_interaction(
        self,
        customer_id: int,
        platform: str,
        message_type: str,
        message_summary: str,
        extracted_info: Dict[str, Any],
        ai_replied: bool = False,
        group_invitation_sent: bool = False
    ) -> CustomerInteraction:
        """
        记录客户交互（不保存详细聊天记录）
        
        Args:
            customer_id: 客户ID
            platform: 平台名称
            message_type: 消息类型
            message_summary: 消息摘要（最多500字符）
            extracted_info: 提取的关键信息
            ai_replied: 是否AI回复
            group_invitation_sent: 是否发送群组邀请
            
        Returns:
            创建的交互记录
        """
        # 截断摘要到500字符
        if len(message_summary) > 500:
            message_summary = message_summary[:497] + "..."
        
        interaction = CustomerInteraction(
            customer_id=customer_id,
            date=date.today(),
            platform=platform,
            message_type=message_type,
            message_summary=message_summary,
            extracted_info=extracted_info,
            ai_replied=ai_replied,
            group_invitation_sent=group_invitation_sent
        )
        
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        
        # 更新每日统计
        self._update_daily_statistics()
        
        return interaction
    
    def mark_joined_group(self, customer_id: int) -> bool:
        """标记客户已加入群组"""
        today = date.today()
        
        # 更新今天的交互记录
        interactions = self.db.query(CustomerInteraction)\
            .filter(
                CustomerInteraction.customer_id == customer_id,
                CustomerInteraction.date == today,
                CustomerInteraction.joined_group == False
            )\
            .all()
        
        for interaction in interactions:
            interaction.joined_group = True
        
        if interactions:
            self.db.commit()
            self._update_daily_statistics()
            return True
        
        return False
    
    def mark_order_created(self, customer_id: int) -> bool:
        """标记客户已开单"""
        today = date.today()
        
        # 更新今天的交互记录
        interactions = self.db.query(CustomerInteraction)\
            .filter(
                CustomerInteraction.customer_id == customer_id,
                CustomerInteraction.date == today,
                CustomerInteraction.order_created == False
            )\
            .all()
        
        for interaction in interactions:
            interaction.order_created = True
        
        if interactions:
            self.db.commit()
            self._update_daily_statistics()
            return True
        
        return False
    
    def record_frequent_question(self, question_text: str, category: str = None, sample_response: str = None):
        """记录高频问题"""
        # 清理问题文本
        question_text = question_text.strip()[:500]
        
        if not question_text:
            return
        
        # 查找或创建问题记录
        question = self.db.query(FrequentQuestion)\
            .filter(FrequentQuestion.question_text == question_text)\
            .first()
        
        if question:
            # 更新出现次数
            question.occurrence_count += 1
            question.last_seen = datetime.now(timezone.utc)
            
            # 更新示例回复（保留最新的几个）
            if sample_response:
                sample_responses = question.sample_responses or []
                sample_responses.append({
                    "response": sample_response[:200],
                    "time": datetime.now(timezone.utc).isoformat()
                })
                # 只保留最近5个
                question.sample_responses = sample_responses[-5:]
        else:
            # 创建新问题
            question = FrequentQuestion(
                question_text=question_text,
                question_category=category,
                occurrence_count=1,
                sample_responses=[{
                    "response": sample_response[:200] if sample_response else None,
                    "time": datetime.now(timezone.utc).isoformat()
                }] if sample_response else []
            )
            self.db.add(question)
        
        self.db.commit()
    
    def _update_daily_statistics(self):
        """更新每日统计数据"""
        today = date.today()
        stats = self.get_or_create_daily_statistics(today)
        
        # 统计今天的客户数
        total_customers = self.db.query(sql_func.count(sql_func.distinct(CustomerInteraction.customer_id)))\
            .filter(CustomerInteraction.date == today)\
            .scalar() or 0
        
        # 统计今天的消息数
        total_messages = self.db.query(sql_func.count(CustomerInteraction.id))\
            .filter(CustomerInteraction.date == today)\
            .scalar() or 0
        
        # 统计发送的群组邀请数
        group_invitations_sent = self.db.query(sql_func.count(CustomerInteraction.id))\
            .filter(
                CustomerInteraction.date == today,
                CustomerInteraction.group_invitation_sent == True
            )\
            .scalar() or 0
        
        # 统计成功引流数（加入群组）
        successful_leads = self.db.query(sql_func.count(sql_func.distinct(CustomerInteraction.customer_id)))\
            .filter(
                CustomerInteraction.date == today,
                CustomerInteraction.joined_group == True
            )\
            .scalar() or 0
        
        # 统计开单数
        total_orders = self.db.query(sql_func.count(CustomerInteraction.id))\
            .filter(
                CustomerInteraction.date == today,
                CustomerInteraction.order_created == True
            )\
            .scalar() or 0
        
        successful_orders = self.db.query(sql_func.count(sql_func.distinct(CustomerInteraction.customer_id)))\
            .filter(
                CustomerInteraction.date == today,
                CustomerInteraction.order_created == True
            )\
            .scalar() or 0
        
        # 计算转化率
        lead_conversion_rate = "0%"
        if group_invitations_sent > 0:
            rate = (successful_leads / group_invitations_sent) * 100
            lead_conversion_rate = f"{rate:.1f}%"
        
        order_conversion_rate = "0%"
        if successful_leads > 0:
            rate = (successful_orders / successful_leads) * 100
            order_conversion_rate = f"{rate:.1f}%"
        
        # 更新统计数据
        stats.total_customers = total_customers
        stats.total_messages = total_messages
        stats.group_invitations_sent = group_invitations_sent
        stats.successful_leads = successful_leads
        stats.lead_conversion_rate = lead_conversion_rate
        stats.total_orders = total_orders
        stats.successful_orders = successful_orders
        stats.order_conversion_rate = order_conversion_rate
        
        self.db.commit()
        self.db.refresh(stats)
    
    def get_daily_statistics(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """获取每日统计数据"""
        if target_date is None:
            target_date = date.today()
        
        stats = self.get_or_create_daily_statistics(target_date)
        
        return {
            "date": stats.date.isoformat(),
            "total_customers": stats.total_customers,
            "new_customers": stats.new_customers,
            "returning_customers": stats.returning_customers,
            "total_messages": stats.total_messages,
            "group_invitations_sent": stats.group_invitations_sent,
            "successful_leads": stats.successful_leads,
            "lead_conversion_rate": stats.lead_conversion_rate,
            "total_orders": stats.total_orders,
            "successful_orders": stats.successful_orders,
            "order_conversion_rate": stats.order_conversion_rate,
            "frequent_questions": stats.frequent_questions or {}
        }
    
    def get_frequent_questions(self, limit: int = 20) -> list:
        """获取高频问题列表"""
        questions = self.db.query(FrequentQuestion)\
            .order_by(FrequentQuestion.occurrence_count.desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                "id": q.id,
                "question": q.question_text,
                "category": q.question_category,
                "count": q.occurrence_count,
                "first_seen": q.first_seen.isoformat() if q.first_seen else None,
                "last_seen": q.last_seen.isoformat() if q.last_seen else None,
                "sample_responses": q.sample_responses or []
            }
            for q in questions
        ]


