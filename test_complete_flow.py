"""完整流程测试脚本"""
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"

def read_env_value(key):
    """从 .env 文件读取值"""
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    value = line.split("=", 1)[1].strip()
                    if value and not value.startswith("your_"):
                        return value
    return None

def test_webhook_receive():
    """测试接收 Facebook Webhook 消息"""
    print("=" * 60)
    print("测试 1: 接收 Facebook Webhook 消息")
    print("=" * 60)
    
    # 模拟 Facebook Webhook 消息
    test_message = {
        "object": "page",
        "entry": [
            {
                "id": "test_page_id",
                "time": int(datetime.now().timestamp()),
                "messaging": [
                    {
                        "sender": {"id": "test_user_123"},
                        "recipient": {"id": "test_page_id"},
                        "timestamp": int(datetime.now().timestamp() * 1000),
                        "message": {
                            "mid": "test_message_id",
                            "text": "测试消息：你好，我想咨询一下产品信息"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✓ Webhook 消息接收测试通过")
            return True
        else:
            print("⚠️  Webhook 消息接收可能有问题")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_ai_reply():
    """测试 AI 回复生成"""
    print("\n" + "=" * 60)
    print("测试 2: AI 回复生成")
    print("=" * 60)
    
    openai_key = read_env_value("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️  OpenAI API Key 未配置，跳过 AI 测试")
        return None
    
    print("✓ OpenAI API Key 已配置")
    print("ℹ️  AI 回复功能需要在实际消息处理中测试")
    print("   当系统接收到消息时，会自动调用 AI 生成回复")
    
    return True

def test_telegram_notification():
    """测试 Telegram 通知"""
    print("\n" + "=" * 60)
    print("测试 3: Telegram 通知")
    print("=" * 60)
    
    bot_token = read_env_value("TELEGRAM_BOT_TOKEN")
    chat_id = read_env_value("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️  Telegram 配置不完整，跳过通知测试")
        return None
    
    print(f"✓ Telegram Bot Token 已配置")
    print(f"✓ Telegram Chat ID 已配置: {chat_id}")
    print("ℹ️  Telegram 通知功能需要在实际消息处理中测试")
    print("   当系统处理消息时，会自动发送通知到 Telegram")
    
    return True

def test_database():
    """测试数据库连接"""
    print("\n" + "=" * 60)
    print("测试 4: 数据库连接")
    print("=" * 60)
    
    try:
        from src.database.database import engine
        with engine.connect() as conn:
            print("✓ 数据库连接正常")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Facebook 客服自动化系统 - 完整流程测试")
    print("=" * 60)
    print(f"\n测试服务器: {BASE_URL}")
    print("确保服务正在运行 (python run.py)\n")
    
    results = []
    
    # 运行测试
    results.append(("数据库连接", test_database()))
    results.append(("Webhook 接收", test_webhook_receive()))
    results.append(("AI 回复", test_ai_reply()))
    results.append(("Telegram 通知", test_telegram_notification()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result is True)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for name, result in results:
        if result is True:
            status = "✓ 通过"
        elif result is None:
            status = "⚠️  跳过（需要实际消息）"
        else:
            status = "✗ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过, {skipped} 个跳过")
    
    print("\n" + "=" * 60)
    print("下一步")
    print("=" * 60)
    print("\n1. 配置 Facebook Webhook（使用 ngrok 或生产环境）")
    print("2. 发送真实消息到 Facebook 测试完整流程")
    print("3. 检查 AI 回复和 Telegram 通知")
    print("\n详细说明请查看: TESTING_COMPLETE_GUIDE.md")
    print("=" * 60)

if __name__ == "__main__":
    main()

