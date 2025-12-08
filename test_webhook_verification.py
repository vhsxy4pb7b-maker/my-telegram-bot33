#!/usr/bin/env python3
"""
Webhook 验证测试工具

用于测试 Webhook 验证端点是否正常工作
"""

import sys
import requests
from urllib.parse import urlencode

def test_webhook_verification(domain: str, verify_token: str):
    """
    测试 Webhook 验证端点
    
    Args:
        domain: Zeabur 域名（例如：my-telegram-bot33.zeabur.app）
        verify_token: 验证令牌
    """
    print("=" * 60)
    print("Webhook 验证测试工具")
    print("=" * 60)
    print()
    
    # 测试 1: 健康检查
    print("测试 1: 健康检查端点")
    print("-" * 60)
    health_url = f"https://{domain}/health"
    print(f"URL: {health_url}")
    
    try:
        response = requests.get(health_url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 健康检查通过")
        else:
            print("❌ 健康检查失败")
            return False
    except Exception as e:
        print(f"❌ 无法访问健康检查端点: {str(e)}")
        return False
    
    print()
    
    # 测试 2: Webhook 验证端点
    print("测试 2: Webhook 验证端点")
    print("-" * 60)
    
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": verify_token,
        "hub.challenge": "test123"
    }
    
    webhook_url = f"https://{domain}/webhook?{urlencode(params)}"
    print(f"URL: {webhook_url}")
    print(f"验证令牌: {verify_token}")
    print(f"预期返回: test123")
    
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200 and response.text.strip() == "test123":
            print("✅ Webhook 验证端点工作正常")
            return True
        elif response.status_code == 403:
            print("❌ 验证失败：验证令牌不匹配")
            print("   请检查验证令牌是否与 Zeabur 环境变量中的值完全一致")
            return False
        elif response.status_code == 404:
            print("❌ 验证失败：URL 路径错误")
            print("   请确认 URL 是：https://域名.zeabur.app/webhook")
            return False
        else:
            print(f"❌ 验证失败：状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问 Webhook 端点: {str(e)}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python test_webhook_verification.py <域名> <验证令牌>")
        print()
        print("示例:")
        print("  python test_webhook_verification.py my-telegram-bot33.zeabur.app my_secure_token_2024")
        print()
        print("参数说明:")
        print("  域名: 你的 Zeabur 域名（不包括 https://）")
        print("  验证令牌: 从 Zeabur 环境变量中获取的 FACEBOOK_VERIFY_TOKEN")
        sys.exit(1)
    
    domain = sys.argv[1]
    verify_token = sys.argv[2]
    
    # 移除域名中的 https:// 前缀（如果有）
    if domain.startswith("https://"):
        domain = domain.replace("https://", "")
    
    # 移除域名末尾的斜杠（如果有）
    if domain.endswith("/"):
        domain = domain.rstrip("/")
    
    success = test_webhook_verification(domain, verify_token)
    
    print()
    print("=" * 60)
    if success:
        print("✅ 所有测试通过！可以在 Facebook 中配置 Webhook 了。")
    else:
        print("❌ 测试失败，请根据上述错误信息排查问题。")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

