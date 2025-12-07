"""检查 Railway 部署配置"""
import os
import sys

def check_env_vars():
    """检查必需的环境变量"""
    required_vars = [
        "FACEBOOK_APP_ID",
        "FACEBOOK_APP_SECRET",
        "FACEBOOK_ACCESS_TOKEN",
        "FACEBOOK_VERIFY_TOKEN",
        "OPENAI_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "SECRET_KEY",
    ]
    
    print("=" * 60)
    print("检查环境变量配置")
    print("=" * 60)
    
    missing = []
    configured = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your_") or value.startswith("你的"):
            missing.append(var)
            print(f"❌ {var}: 未配置或为占位符")
        else:
            configured.append(var)
            # 只显示前几个字符，保护隐私
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
    
    print("\n" + "=" * 60)
    if missing:
        print(f"⚠️  缺少 {len(missing)} 个必需的环境变量:")
        for var in missing:
            print(f"   - {var}")
        print("\n请在 Railway Variables 中添加这些变量")
        return False
    else:
        print("✅ 所有必需的环境变量已配置")
        return True

def check_files():
    """检查必需的文件"""
    required_files = [
        "railway.json",
        "Procfile",
        "requirements.txt",
        "src/main.py",
    ]
    
    print("\n" + "=" * 60)
    print("检查必需文件")
    print("=" * 60)
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: 存在")
        else:
            missing.append(file)
            print(f"❌ {file}: 不存在")
    
    if missing:
        print(f"\n⚠️  缺少 {len(missing)} 个必需的文件")
        return False
    else:
        print("\n✅ 所有必需的文件都存在")
        return True

def check_database_config():
    """检查数据库配置"""
    print("\n" + "=" * 60)
    print("检查数据库配置")
    print("=" * 60)
    
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if "postgresql" in db_url.lower() or "postgres" in db_url.lower():
            print("✅ DATABASE_URL: 已配置（PostgreSQL）")
            return True
        else:
            print("⚠️  DATABASE_URL: 已配置，但不是 PostgreSQL")
            return False
    else:
        print("❌ DATABASE_URL: 未配置")
        print("   请在 Railway 中添加 PostgreSQL 数据库")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Railway 部署配置检查")
    print("=" * 60)
    print()
    
    results = []
    
    # 检查文件
    results.append(("文件检查", check_files()))
    
    # 检查环境变量（如果在 Railway 环境）
    if os.getenv("RAILWAY_ENVIRONMENT"):
        results.append(("环境变量", check_env_vars()))
        results.append(("数据库配置", check_database_config()))
    else:
        print("\n" + "=" * 60)
        print("环境变量检查")
        print("=" * 60)
        print("ℹ️  当前不在 Railway 环境中")
        print("   环境变量检查将在 Railway 部署时自动进行")
    
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
        print("✅ 所有检查通过！可以部署到 Railway")
    else:
        print("⚠️  部分检查未通过，请修复后重试")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())


