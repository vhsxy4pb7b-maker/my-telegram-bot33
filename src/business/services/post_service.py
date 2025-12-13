"""
发帖服务接口（预留）
为自动发帖功能预留接口，待后续实现
"""
from typing import Dict, Any, Optional
from .base_service import BaseBusinessService
import logging

logger = logging.getLogger(__name__)


class PostService(BaseBusinessService):
    """发帖服务接口（预留）"""
    
    def __init__(self):
        super().__init__("post_service", "发帖服务（预留接口）")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行发帖业务逻辑（预留接口，待实现）
        
        Args:
            context: 执行上下文，包含：
                - content: 帖子内容
                - platform: 平台（facebook/instagram）
                - page_id: 页面ID
                - material_generator: 素材生成服务（可选）
        
        Returns:
            执行结果字典
        """
        logger.warning("PostService.execute() 尚未实现，这是预留接口")
        return {
            "success": False,
            "message": "发帖服务尚未实现，请等待后续开发"
        }
    
    async def post_to_facebook(self, page_id: str, content: str, 
                               material_generator: Optional[Any] = None) -> Dict[str, Any]:
        """
        发布Facebook帖子（预留接口）
        
        Args:
            page_id: 页面ID
            content: 帖子内容
            material_generator: 素材生成服务（可选）
        
        Returns:
            发布结果
        """
        raise NotImplementedError("post_to_facebook() 尚未实现")
    
    async def post_reel_to_instagram(self, user_id: str, content: str,
                                    material_generator: Optional[Any] = None) -> Dict[str, Any]:
        """
        发布Instagram Reels（预留接口）
        
        Args:
            user_id: Instagram用户ID
            content: Reels内容
            material_generator: 素材生成服务（可选）
        
        Returns:
            发布结果
        """
        raise NotImplementedError("post_reel_to_instagram() 尚未实现")

