"""测试数据验证器"""
import pytest
from src.collector.data_validator import DataValidator


def test_validate_email():
    """测试邮箱验证"""
    validator = DataValidator()
    
    # 有效邮箱
    is_valid, error = validator.validate_email("test@example.com")
    assert is_valid is True
    assert error is None
    
    # 无效邮箱
    is_valid, error = validator.validate_email("invalid-email")
    assert is_valid is False
    assert error is not None


def test_validate_phone():
    """测试电话验证"""
    validator = DataValidator()
    
    # 中国手机号
    is_valid, error = validator.validate_phone("13800138000")
    assert is_valid is True
    
    # 无效电话
    is_valid, error = validator.validate_phone("123")
    assert is_valid is False


def test_extract_email():
    """测试邮箱提取"""
    validator = DataValidator()
    
    text = "我的邮箱是 test@example.com，请联系我"
    email = validator.extract_email(text)
    assert email == "test@example.com"


def test_extract_phone():
    """测试电话提取"""
    validator = DataValidator()
    
    text = "我的电话是 13800138000"
    phone = validator.extract_phone(text)
    assert phone == "13800138000"


