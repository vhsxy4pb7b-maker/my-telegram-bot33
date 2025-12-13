"""
业务服务基类
所有业务服务都应继承此类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseBusinessService(ABC):
    """业务服务基类"""
    
    def __init__(self, name: str, description: str = ""):
        """
        初始化业务服务
        
        Args:
            name: 服务名称
            description: 服务描述
        """
        self.name = name
        self.description = description
        self._enabled = True
    
    @property
    def enabled(self) -> bool:
        """服务是否启用"""
        return self._enabled
    
    def enable(self):
        """启用服务"""
        self._enabled = True
        logger.info(f"业务服务 {self.name} 已启用")
    
    def disable(self):
        """禁用服务"""
        self._enabled = False
        logger.info(f"业务服务 {self.name} 已禁用")
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行业务逻辑（抽象方法，子类必须实现）
        
        Args:
            context: 执行上下文，包含所需的所有数据
            
        Returns:
            执行结果字典
        """
        pass
    
    def validate(self, context: Dict[str, Any]) -> Optional[str]:
        """
        验证执行条件（可选实现）
        
        Args:
            context: 执行上下文
            
        Returns:
            如果验证失败，返回错误消息；否则返回None
        """
        if not self._enabled:
            return f"业务服务 {self.name} 未启用"
        return None
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"

