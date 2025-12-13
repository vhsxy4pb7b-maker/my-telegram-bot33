"""统一异常处理"""
from typing import Optional, Dict, Any


class AppException(Exception):
    """应用基础异常类"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error": self.message,
            "error_code": self.error_code,
            "details": self.details
        }


class ValidationError(AppException):
    """验证错误"""
    
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)
        if field:
            self.details["field"] = field


class APIError(AppException):
    """API调用错误"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        api_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="API_ERROR", **kwargs)
        if status_code:
            self.details["status_code"] = status_code
        if api_name:
            self.details["api_name"] = api_name


class DatabaseError(AppException):
    """数据库错误"""
    
    def __init__(self, message: str, operation: Optional[str] = None, **kwargs):
        super().__init__(message, error_code="DATABASE_ERROR", **kwargs)
        if operation:
            self.details["operation"] = operation


class ProcessingError(AppException):
    """消息处理流程中的错误"""
    
    def __init__(self, message: str, step: Optional[str] = None, **kwargs):
        super().__init__(message, error_code="PROCESSING_ERROR", **kwargs)
        if step:
            self.details["step"] = step

