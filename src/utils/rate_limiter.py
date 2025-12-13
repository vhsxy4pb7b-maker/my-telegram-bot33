"""请求限流器"""
import time
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta


class RateLimiter:
    """简单的内存限流器（生产环境建议使用Redis）"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits: Dict[str, tuple] = {}  # key -> (max_requests, time_window_seconds)
    
    def set_limit(
        self,
        key: str,
        max_requests: int,
        time_window_seconds: int = 60
    ) -> None:
        """
        设置限流规则
        
        Args:
            key: 限流键（如IP地址、用户ID等）
            max_requests: 时间窗口内最大请求数
            time_window_seconds: 时间窗口（秒）
        """
        self.limits[key] = (max_requests, time_window_seconds)
    
    def is_allowed(
        self,
        key: str,
        default_max: int = 100,
        default_window: int = 60
    ) -> bool:
        """
        检查是否允许请求
        
        Args:
            key: 限流键
            default_max: 默认最大请求数
            default_window: 默认时间窗口
        
        Returns:
            是否允许请求
        """
        max_requests, window = self.limits.get(
            key,
            (default_max, default_window)
        )
        
        now = time.time()
        cutoff = now - window
        
        # 清理过期记录
        self.requests[key] = [
            timestamp for timestamp in self.requests[key]
            if timestamp > cutoff
        ]
        
        # 检查是否超过限制
        if len(self.requests[key]) >= max_requests:
            return False
        
        # 记录本次请求
        self.requests[key].append(now)
        return True
    
    def get_remaining(
        self,
        key: str,
        default_max: int = 100,
        default_window: int = 60
    ) -> int:
        """
        获取剩余请求次数
        
        Args:
            key: 限流键
            default_max: 默认最大请求数
            default_window: 默认时间窗口
        
        Returns:
            剩余请求次数
        """
        max_requests, window = self.limits.get(
            key,
            (default_max, default_window)
        )
        
        now = time.time()
        cutoff = now - window
        
        # 清理过期记录
        self.requests[key] = [
            timestamp for timestamp in self.requests[key]
            if timestamp > cutoff
        ]
        
        return max(0, max_requests - len(self.requests[key]))
    
    def reset(self, key: Optional[str] = None) -> None:
        """
        重置限流记录
        
        Args:
            key: 要重置的键，如果为None则重置所有
        """
        if key:
            self.requests.pop(key, None)
        else:
            self.requests.clear()


# 全局限流器实例
rate_limiter = RateLimiter()

