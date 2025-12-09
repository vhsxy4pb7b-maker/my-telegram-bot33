"""Facebook Graph API 客户端"""
import httpx
from typing import Dict, Any, Optional
from src.config import settings


class FacebookAPIClient:
    """Facebook Graph API 客户端封装"""
    
    def __init__(self):
        self.access_token = settings.facebook_access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_message(
        self,
        recipient_id: str,
        message: str,
        message_type: str = "RESPONSE"
    ) -> Dict[str, Any]:
        """
        发送消息到 Facebook
        
        Args:
            recipient_id: 接收者 Facebook ID
            message: 消息内容
            message_type: 消息类型 (RESPONSE, UPDATE, MESSAGE_TAG)
        
        Returns:
            API 响应
        """
        url = f"{self.base_url}/me/messages"
        params = {"access_token": self.access_token}
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "messaging_type": message_type
        }
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户信息
        
        Args:
            user_id: Facebook 用户 ID
        
        Returns:
            用户信息
        """
        url = f"{self.base_url}/{user_id}"
        params = {
            "access_token": self.access_token,
            "fields": "id,name,first_name,last_name,profile_pic"
        }
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def comment_on_post(
        self,
        post_id: str,
        message: str
    ) -> Dict[str, Any]:
        """
        在帖子下评论
        
        Args:
            post_id: 帖子 ID
            message: 评论内容
        
        Returns:
            API 响应
        """
        url = f"{self.base_url}/{post_id}/comments"
        params = {"access_token": self.access_token}
        data = {"message": message}
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    async def verify_webhook(
        self,
        mode: str,
        token: str,
        challenge: str
    ) -> Optional[str]:
        """
        验证 Webhook 订阅
        
        Args:
            mode: 验证模式
            token: 验证令牌
            challenge: 挑战字符串
        
        Returns:
            如果验证成功返回 challenge，否则返回 None
        """
        if mode == "subscribe" and token == settings.facebook_verify_token:
            return challenge
        return None
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()


