"""Instagram 消息解析器"""
from typing import Dict, Any, Optional, List
from src.database.models import MessageType
from src.platforms.base import PlatformParser


class InstagramMessageParser(PlatformParser):
    """解析 Instagram Webhook 消息"""
    
    def parse_webhook_event(self, event: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        解析Webhook事件
        
        Args:
            event: Instagram Webhook 事件数据
        
        Returns:
            解析后的消息数据列表，如果无法解析则返回None
        """
        # Instagram使用与Facebook相同的Webhook结构，但object为"instagram"
        if "object" not in event or event["object"] != "instagram":
            return None
        
        entries = event.get("entry", [])
        if not entries:
            return None
        
        parsed_messages = []
        
        for entry in entries:
            # 处理Instagram私信事件
            messaging_events = entry.get("messaging", [])
            for messaging_event in messaging_events:
                message_data = self._parse_messaging_event(
                    messaging_event, entry.get("id")
                )
                if message_data:
                    parsed_messages.append(message_data)
        
        return parsed_messages if parsed_messages else None
    
    def _parse_messaging_event(
        self,
        event: Dict[str, Any],
        page_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """解析Instagram私信事件"""
        sender = event.get("sender", {})
        recipient = event.get("recipient", {})
        message = event.get("message", {})
        
        if not message or "text" not in message:
            return None
        
        return {
            "message_id": message.get("mid"),
            "sender_id": sender.get("id"),
            "recipient_id": recipient.get("id"),
            "page_id": page_id,
            "message_type": MessageType.MESSAGE,
            "content": message.get("text"),
            "timestamp": event.get("timestamp"),
            "raw_data": event
        }
    
    def extract_user_info(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """从事件中提取用户信息"""
        sender = event.get("sender", {})
        
        return {
            "instagram_id": sender.get("id"),
            "username": sender.get("username"),
            "name": sender.get("name")
        }

