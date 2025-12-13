"""
客服业务模块工作流定义
定义客服业务的各种工作流程
"""
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class CustomerServiceWorkflow:
    """客服业务工作流"""
    
    def __init__(self):
        self.workflow_name = "customer_service_workflow"
    
    def get_message_processing_workflow(self) -> List[str]:
        """
        获取消息处理工作流步骤
        
        Returns:
            工作流步骤列表
        """
        return [
            "message_receive",      # 消息接收
            "user_info_handler",    # 用户信息处理
            "filter_handler",       # 过滤处理
            "ai_reply_handler",     # AI回复
            "data_collection",      # 数据收集
            "statistics_handler",   # 统计记录
            "notification_handler"  # 通知发送
        ]
    
    def get_review_workflow(self) -> List[str]:
        """
        获取审核工作流步骤
        
        Returns:
            工作流步骤列表
        """
        return [
            "filter_check",         # 过滤检查
            "priority_check",       # 优先级检查
            "telegram_notification", # Telegram通知
            "manual_review"         # 人工审核
        ]


# 全局工作流实例
customer_service_workflow = CustomerServiceWorkflow()

