"""工具注册器 - 管理所有可用工具"""
from typing import Dict, Type, Optional
from .base import BaseTool


class ToolRegistry:
    """工具注册器（单例模式）"""
    
    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, name: str, tool_class: Type[BaseTool]):
        """
        注册工具
        
        Args:
            name: 工具名称
            tool_class: 工具类
        """
        self._tools[name] = tool_class
    
    def get(self, name: str) -> Optional[Type[BaseTool]]:
        """
        获取工具类
        
        Args:
            name: 工具名称
            
        Returns:
            工具类，如果不存在则返回None
        """
        return self._tools.get(name)
    
    def list_tools(self) -> list:
        """
        列出所有已注册的工具
        
        Returns:
            工具名称列表
        """
        return list(self._tools.keys())
    
    def create_tool(self, name: str, **kwargs) -> Optional[BaseTool]:
        """
        创建工具实例
        
        Args:
            name: 工具名称
            **kwargs: 工具初始化参数
            
        Returns:
            工具实例，如果不存在则返回None
        """
        tool_class = self.get(name)
        if tool_class:
            return tool_class(**kwargs)
        return None


# 全局注册器实例
registry = ToolRegistry()

# 自动注册内置工具
from .token_manager import TokenManager
from .config_checker import ConfigChecker
from .permission_checker import PermissionChecker
from .exchange_token_tool import ExchangeTokenTool

registry.register("token_manager", TokenManager)
registry.register("config_checker", ConfigChecker)
registry.register("permission_checker", PermissionChecker)
registry.register("exchange_token", ExchangeTokenTool)

