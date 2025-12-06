"""平台抽象层模块"""
from src.platforms.base import (
    PlatformClient,
    PlatformParser,
    PlatformWebhookHandler
)
from src.platforms.registry import PlatformRegistry, registry
from src.platforms.manager import PlatformManager, platform_manager

__all__ = [
    "PlatformClient",
    "PlatformParser",
    "PlatformWebhookHandler",
    "PlatformRegistry",
    "registry",
    "PlatformManager",
    "platform_manager",
]
