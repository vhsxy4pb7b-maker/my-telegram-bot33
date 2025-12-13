"""
业务服务层模块
提供业务逻辑抽象和服务接口
"""
from .registry import business_registry

# 注册AI自动回复服务
from .services.auto_reply_service import AutoReplyService
business_registry.register("auto_reply", AutoReplyService)

__all__ = ['business_registry']
