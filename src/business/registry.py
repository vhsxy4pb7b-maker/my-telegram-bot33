"""
业务服务注册器
管理所有业务服务的注册和获取
"""
from typing import Dict, Type, Optional, List
from .services.base_service import BaseBusinessService
import logging

logger = logging.getLogger(__name__)


class BusinessRegistry:
    """业务服务注册器（单例模式）"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BusinessRegistry, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._services: Dict[str, BaseBusinessService] = {}
            self._service_classes: Dict[str, Type[BaseBusinessService]] = {}
            self._initialized = True
    
    def register(self, name: str, service_class: Type[BaseBusinessService]):
        """
        注册业务服务类
        
        Args:
            name: 服务名称
            service_class: 服务类
        """
        self._service_classes[name] = service_class
        logger.debug(f"注册业务服务类: {name} -> {service_class.__name__}")
    
    def register_instance(self, name: str, service_instance: BaseBusinessService):
        """
        注册业务服务实例
        
        Args:
            name: 服务名称
            service_instance: 服务实例
        """
        self._services[name] = service_instance
        logger.debug(f"注册业务服务实例: {name}")
    
    def get(self, name: str) -> Optional[BaseBusinessService]:
        """
        获取业务服务实例
        
        Args:
            name: 服务名称
            
        Returns:
            服务实例，如果不存在则返回None
        """
        # 先查找已注册的实例
        if name in self._services:
            return self._services[name]
        
        # 如果不存在实例，尝试创建新实例
        if name in self._service_classes:
            service_class = self._service_classes[name]
            instance = service_class()
            self._services[name] = instance
            return instance
        
        logger.warning(f"业务服务 {name} 未注册")
        return None
    
    def list_services(self) -> List[str]:
        """列出所有已注册的服务名称"""
        all_services = set(self._services.keys()) | set(self._service_classes.keys())
        return list(all_services)
    
    def unregister(self, name: str):
        """
        取消注册业务服务
        
        Args:
            name: 服务名称
        """
        if name in self._services:
            del self._services[name]
        if name in self._service_classes:
            del self._service_classes[name]
        logger.debug(f"取消注册业务服务: {name}")


# 全局业务服务注册器实例
business_registry = BusinessRegistry()

