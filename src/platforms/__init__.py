"""平台抽象层模块"""
# 延迟导入以避免循环依赖
# 这些类可能不存在，使用延迟导入或占位符
try:
    from src.platforms.base import (
        PlatformClient,
        PlatformParser,
        PlatformWebhookHandler
    )
except ImportError:
    # 如果base模块不存在，创建占位符类
    class PlatformClient:
        """平台客户端基类（占位符）"""
        pass
    
    class PlatformParser:
        """平台解析器基类（占位符）"""
        pass
    
    class PlatformWebhookHandler:
        """平台Webhook处理器基类（占位符）"""
        pass

# 先导入 registry（manager 依赖它）
from src.platforms.registry import PlatformRegistry, registry

# 延迟导入 manager 以避免可能的循环导入问题
# 使用 __getattr__ 实现延迟导入
def __getattr__(name):
    if name in ("PlatformManager", "platform_manager"):
        # 延迟导入，避免在模块初始化时立即导入
        from src.platforms.manager import PlatformManager as _PlatformManager
        from src.platforms.manager import platform_manager as _platform_manager
        
        # 将导入的对象缓存到模块命名空间
        import sys
        current_module = sys.modules[__name__]
        setattr(current_module, "PlatformManager", _PlatformManager)
        setattr(current_module, "platform_manager", _platform_manager)
        
        if name == "PlatformManager":
            return _PlatformManager
        elif name == "platform_manager":
            return _platform_manager
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "PlatformClient",
    "PlatformParser",
    "PlatformWebhookHandler",
    "PlatformRegistry",
    "registry",
    "PlatformManager",
    "platform_manager",
]
