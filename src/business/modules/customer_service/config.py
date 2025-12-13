"""
客服业务模块配置
"""
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class CustomerServiceConfig:
    """客服业务模块配置"""
    
    def __init__(self):
        self.module_name = "customer_service"
        self.description = "客服业务模块"
        self.enabled = True
        
        # 模块功能配置
        self.features = {
            "auto_reply": True,      # AI自动回复
            "data_collection": True,  # 数据收集
            "filtering": True,        # 智能过滤
            "notification": True,     # 通知审核
        }
    
    def get_config(self) -> Dict[str, Any]:
        """获取模块配置"""
        return {
            "module_name": self.module_name,
            "description": self.description,
            "enabled": self.enabled,
            "features": self.features
        }
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """检查功能是否启用"""
        return self.features.get(feature_name, False)


# 全局配置实例
customer_service_config = CustomerServiceConfig()

