"""检查 Zeabur 环境变量配置"""
import os
import sys

def check_env_var(name, description, is_required=True, check_placeholder=True):
    """检查环境变量"""
    value = os.getenv(name)
    
    if not value:
        if is_required:
            print(f"❌ {name}: 未设置 - {description}")
            return False
        else:
            print(f"⚠️  {name}: 未设置（可选）")
            return True
    
    # 检查占位符
    if check_placeholder:
        placeholders = [
            "your_", "你的", "placeholder", "example", 
            "replace", "change", "set_here"
        ]
        if any(placeholder in value.lower() for placeholder in placeholders):
            print(f"❌ {name}: 是占位符 - {description}")
            print(f"   当前值: {value[:50]}...")
            return False
    
    # 显示部分值（保护隐私）
    display_value = value[:20] + "..." if len(value) > 20 else value
    print(f"✅ {name}: 已设置 - {display_value}")
    return True

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Zeabur 环境变量检查")
    print("=" * 60)
    print("\n注意: 此检查在本地运行，实际环境变量在 Zeabur 中配置")
    print("=" * 60)
    
    print("\n必需的环境变量：")
    print("-" * 60)
    
    results = []
    
    # 检查必需变量
    results.append(("DATABASE_URL", check_env_var(
        "DATABASE_URL", 
        "数据库连接字符串（由 Zeabur 自动设置）",
        is_required=True,
        check_placeholder=False
    )))
    
    results.append(("FACEBOOK_APP_ID", check_env_var(
        "FACEBOOK_APP_ID",
        "Facebook 应用 ID"
    )))
    
    results.append(("FACEBOOK_APP_SECRET", check_env_var(
        "FACEBOOK_APP_SECRET",
        "Facebook 应用密钥"
    )))
    
    results.append(("FACEBOOK_ACCESS_TOKEN", check_env_var(
        "FACEBOOK_ACCESS_TOKEN",
        "Facebook 访问令牌"
    )))
    
    results.append(("FACEBOOK_VERIFY_TOKEN", check_env_var(
        "FACEBOOK_VERIFY_TOKEN",
        "Facebook 验证令牌（可以是任意字符串）",
        check_placeholder=False
    )))
    
    results.append(("OPENAI_API_KEY", check_env_var(
        "OPENAI_API_KEY",
        "OpenAI API 密钥（应该以 sk- 开头）"
    )))
    
    results.append(("TELEGRAM_BOT_TOKEN", check_env_var(
        "TELEGRAM_BOT_TOKEN",
        "Telegram Bot 令牌"
    )))
    
    results.append(("TELEGRAM_CHAT_ID", check_env_var(
        "TELEGRAM_CHAT_ID",
        "Telegram 聊天 ID"
    )))
    
    results.append(("SECRET_KEY", check_env_var(
        "SECRET_KEY",
        "应用密钥",
        check_placeholder=False
    )))
    
    # 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有环境变量检查通过！")
        print("\n注意: 这只是本地检查，实际配置在 Zeabur 中")
    else:
        print("⚠️  部分环境变量未正确配置")
        print("\n请在 Zeabur 项目页面 → Environment Variables 中：")
        print("1. 添加缺失的变量")
        print("2. 将占位符替换为真实值")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())


