"""Telegram 通知发送器"""
import httpx
from typing import Dict, Any, Optional
from src.config import settings, yaml_config
from src.database.models import Conversation, Customer, CollectedData
import logging

logger = logging.getLogger(__name__)


class NotificationSender:
    """向 Telegram 发送审核通知"""

    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.client = httpx.AsyncClient(timeout=30.0)
        self.notification_config = yaml_config.get("telegram", {})

    async def send_review_notification(
        self,
        conversation: Conversation,
        customer: Customer,
        collected_data: Optional[CollectedData] = None
    ) -> bool:
        """
        发送审核通知

        Args:
            conversation: 对话记录
            customer: 客户信息
            collected_data: 收集的数据（可选）

        Returns:
            是否发送成功
        """
        try:
            message = self._format_notification_message(
                conversation,
                customer,
                collected_data
            )

            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": self.notification_config.get("notification_format", "Markdown")
            }

            response = await self.client.post(url, json=data)
            response.raise_for_status()

            logger.info(
                f"Sent review notification for conversation {conversation.id}")
            return True

        except Exception as e:
            logger.error(
                f"Error sending Telegram notification: {str(e)}", exc_info=True)
            return False

    def _format_notification_message(
        self,
        conversation: Conversation,
        customer: Customer,
        collected_data: Optional[CollectedData]
    ) -> str:
        """
        格式化通知消息

        Args:
            conversation: 对话记录
            customer: 客户信息
            collected_data: 收集的数据

        Returns:
            格式化的消息文本
        """
        lines = []

        # 标题
        lines.append("🔔 *新消息需要审核*")
        lines.append("")

        # 客户信息
        if self.notification_config.get("include_customer_info", True):
            lines.append("*客户信息:*")
            if customer.name:
                lines.append(f"姓名: {customer.name}")
            if customer.email:
                lines.append(f"邮箱: {customer.email}")
            if customer.phone:
                lines.append(f"电话: {customer.phone}")
            lines.append(f"Facebook ID: `{customer.facebook_id}`")
            lines.append("")

        # 消息内容
        lines.append("*消息内容:*")
        content = conversation.content
        max_length = self.notification_config.get("max_preview_length", 200)
        if len(content) > max_length and self.notification_config.get("include_message_preview", True):
            content = content[:max_length] + "..."
        lines.append(content)
        lines.append("")

        # 消息类型和优先级
        if conversation.message_type:
            lines.append(f"类型: {conversation.message_type.value}")
        else:
            lines.append(f"类型: 未知")
        if conversation.priority:
            lines.append(f"优先级: {conversation.priority.value.upper()}")
        else:
            lines.append(f"优先级: 未设置")
        lines.append("")

        # 收集的数据
        if collected_data and collected_data.data:
            lines.append("*收集的资料:*")
            for key, value in collected_data.data.items():
                if value:
                    lines.append(f"{key}: {value}")
            lines.append("")

        # 操作提示
        lines.append("*操作命令:*")
        lines.append(f"/approve_{conversation.id} - 通过")
        lines.append(f"/reject_{conversation.id} - 拒绝")
        lines.append(f"/review_{conversation.id} - 查看详情")

        return "\n".join(lines)

    async def send_ai_suggestion(
        self,
        conversation_id: int,
        suggestion: str
    ) -> bool:
        """
        发送 AI 辅助建议

        Args:
            conversation_id: 对话 ID
            suggestion: AI 建议

        Returns:
            是否发送成功
        """
        try:
            message = f"🤖 *AI 辅助建议*\n\n对话 ID: {conversation_id}\n\n{suggestion}"

            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            response = await self.client.post(url, json=data)
            response.raise_for_status()

            return True

        except Exception as e:
            logger.error(
                f"Error sending AI suggestion: {str(e)}", exc_info=True)
            return False

    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
