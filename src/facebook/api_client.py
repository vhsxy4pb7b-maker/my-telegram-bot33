"""Facebook Graph API 客户端"""
from typing import Dict, Any, Optional
from src.platforms.base import PlatformClient


class FacebookAPIClient(PlatformClient):
    """Facebook Graph API 客户端封装"""
    
    def __init__(self, access_token: str = None, base_url: str = None):
        """
        初始化Facebook API客户端
        
        Args:
            access_token: Facebook访问令牌（如果为None，从配置读取）
            base_url: API基础URL（如果为None，使用默认值）
        """
        from src.config import settings
        
        if access_token is None:
            access_token = settings.facebook_access_token
        
        if base_url is None:
            base_url = "https://graph.facebook.com/v18.0"
        
        super().__init__(access_token, base_url)
    
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
    
    async def create_post(
        self,
        page_id: str,
        message: str,
        link: Optional[str] = None,
        published: bool = True
    ) -> Dict[str, Any]:
        """
        发布帖子到Facebook页面
        
        Args:
            page_id: Facebook页面ID
            message: 帖子内容
            link: 链接URL（可选）
            published: 是否立即发布（默认True）
        
        Returns:
            API响应，包含创建的帖子ID
        """
        url = f"{self.base_url}/{page_id}/feed"
        params = {"access_token": self.access_token}
        data = {
            "message": message,
            "published": published
        }
        
        if link:
            data["link"] = link
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    async def delete_post(
        self,
        post_id: str
    ) -> Dict[str, Any]:
        """
        删除Facebook帖子
        
        Args:
            post_id: 要删除的帖子ID
        
        Returns:
            API响应
        """
        url = f"{self.base_url}/{post_id}"
        params = {"access_token": self.access_token}
        
        response = await self.client.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "post_id": post_id}
    
    async def get_post(
        self,
        post_id: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取帖子信息
        
        Args:
            post_id: 帖子ID
            fields: 要获取的字段（逗号分隔），默认获取基本信息
        
        Returns:
            帖子信息
        """
        url = f"{self.base_url}/{post_id}"
        params = {"access_token": self.access_token}
        
        if fields:
            params["fields"] = fields
        else:
            params["fields"] = "id,message,created_time,updated_time,likes,comments,shares"
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # ========== 广告管理功能 ==========
    
    async def get_ad_accounts(self) -> Dict[str, Any]:
        """
        获取广告账户列表
        
        Returns:
            广告账户列表
        """
        url = f"{self.base_url}/me/adaccounts"
        params = {
            "access_token": self.access_token,
            "fields": "id,name,account_id,account_status,currency"
        }
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_ads(
        self,
        ad_account_id: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取广告列表
        
        Args:
            ad_account_id: 广告账户ID
            fields: 要获取的字段（可选）
        
        Returns:
            广告列表
        """
        url = f"{self.base_url}/act_{ad_account_id}/ads"
        params = {"access_token": self.access_token}
        
        if fields:
            params["fields"] = fields
        else:
            params["fields"] = "id,name,status,effective_status,adset_id,campaign_id"
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_ad(
        self,
        ad_id: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取单个广告信息
        
        Args:
            ad_id: 广告ID
            fields: 要获取的字段（可选）
        
        Returns:
            广告信息
        """
        url = f"{self.base_url}/{ad_id}"
        params = {"access_token": self.access_token}
        
        if fields:
            params["fields"] = fields
        else:
            params["fields"] = "id,name,status,effective_status,adset_id,campaign_id,creative"
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def create_ad(
        self,
        ad_account_id: str,
        adset_id: str,
        creative_id: str,
        name: str,
        status: str = "PAUSED"
    ) -> Dict[str, Any]:
        """
        创建广告
        
        Args:
            ad_account_id: 广告账户ID
            adset_id: 广告组ID
            creative_id: 创意ID
            name: 广告名称
            status: 广告状态（PAUSED, ACTIVE等）
        
        Returns:
            创建的广告信息
        """
        url = f"{self.base_url}/act_{ad_account_id}/ads"
        params = {"access_token": self.access_token}
        data = {
            "name": name,
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status": status
        }
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    async def update_ad(
        self,
        ad_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        更新广告
        
        Args:
            ad_id: 广告ID
            name: 新名称（可选）
            status: 新状态（可选）
        
        Returns:
            API响应
        """
        url = f"{self.base_url}/{ad_id}"
        params = {"access_token": self.access_token}
        data = {}
        
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        
        if not data:
            return {"success": False, "error": "No fields to update"}
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    async def delete_ad(
        self,
        ad_id: str
    ) -> Dict[str, Any]:
        """
        删除广告
        
        Args:
            ad_id: 广告ID
        
        Returns:
            API响应
        """
        url = f"{self.base_url}/{ad_id}"
        params = {"access_token": self.access_token}
        
        response = await self.client.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "ad_id": ad_id}
    
    async def get_campaigns(
        self,
        ad_account_id: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取广告系列列表
        
        Args:
            ad_account_id: 广告账户ID
            fields: 要获取的字段（可选）
        
        Returns:
            广告系列列表
        """
        url = f"{self.base_url}/act_{ad_account_id}/campaigns"
        params = {"access_token": self.access_token}
        
        if fields:
            params["fields"] = fields
        else:
            params["fields"] = "id,name,status,objective,spend_cap"
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_adsets(
        self,
        ad_account_id: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取广告组列表
        
        Args:
            ad_account_id: 广告账户ID
            fields: 要获取的字段（可选）
        
        Returns:
            广告组列表
        """
        url = f"{self.base_url}/act_{ad_account_id}/adsets"
        params = {"access_token": self.access_token}
        
        if fields:
            params["fields"] = fields
        else:
            params["fields"] = "id,name,status,campaign_id,daily_budget,lifetime_budget"
        
        response = await self.client.get(url, params=params)
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
        from src.config import settings
        verify_token = settings.facebook_verify_token
        
        if mode == "subscribe" and token == verify_token:
            return challenge
        return None
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()


