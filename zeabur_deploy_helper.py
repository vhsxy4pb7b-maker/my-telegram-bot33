"""Zeabur 部署辅助工具"""
import os
import sys
import subprocess

def print_step(step_num, title):
    """打印步骤标题"""
    print("\n" + "=" * 60)
    print(f"步骤 {step_num}: {title}")
    print("=" * 60)

def check_zeabur_cli():
    """检查 Zeabur CLI 是否安装"""
    try:
        result = subprocess.run(
            ["zeabur", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Zeabur CLI 已安装")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Zeabur CLI 未安装")
    print("\n安装命令:")
    print("  npm i -g @zeabur/cli")
    return False

def show_env_vars_guide():
    """显示环境变量配置指南"""
    print("\n" + "=" * 60)
    print("环境变量配置指南")
    print("=" * 60)
    print("\n请在 Zeabur 项目页面 → Environment Variables 中添加以下变量：\n")
    
    env_vars = [
        ("FACEBOOK_APP_ID", "你的Facebook应用ID"),
        ("FACEBOOK_APP_SECRET", "你的Facebook应用密钥"),
        ("FACEBOOK_ACCESS_TOKEN", "你的Facebook访问令牌"),
        ("FACEBOOK_VERIFY_TOKEN", "你的Facebook验证令牌（自定义字符串，例如: my_verify_token_123）"),
        ("OPENAI_API_KEY", "你的OpenAI API密钥"),
        ("TELEGRAM_BOT_TOKEN", "你的Telegram Bot令牌"),
        ("TELEGRAM_CHAT_ID", "你的Telegram聊天ID"),
        ("SECRET_KEY", "YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U（已生成）"),
    ]
    
    for var, desc in env_vars:
        print(f"  {var:30} = {desc}")
    
    print("\n注意: DATABASE_URL 由 Zeabur 自动设置，无需手动添加")

def show_zeabur_commands():
    """显示 Zeabur CLI 命令"""
    print("\n" + "=" * 60)
    print("Zeabur CLI 常用命令")
    print("=" * 60)
    print("\n1. 登录 Zeabur:")
    print("   zeabur login")
    print("\n2. 链接项目:")
    print("   zeabur link")
    print("\n3. 运行数据库迁移:")
    print("   zeabur exec alembic upgrade head")
    print("\n4. 查看日志:")
    print("   zeabur logs")
    print("\n5. 查看变量:")
    print("   zeabur variables")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Zeabur 部署辅助工具")
    print("=" * 60)
    
    print_step(1, "检查环境")
    
    # 检查 Zeabur CLI
    has_cli = check_zeabur_cli()
    
    # 检查 Git
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        )
        if "github.com" in result.stdout.lower():
            print("✅ Git 远程仓库已配置")
    except:
        pass
    
    print_step(2, "部署步骤")
    print("\n由于 Zeabur 部署需要在网页上操作，请按照以下步骤：")
    print("\n1. 访问 https://zeabur.com")
    print("2. 登录（使用 GitHub 账号）")
    print("3. 点击 'New Project' 或 '+'")
    print("4. 选择 'Import from GitHub'")
    print("5. 选择仓库: vhsxy4pb7b-maker/my-telegram-bot33")
    print("6. 等待部署开始")
    
    print_step(3, "添加数据库")
    print("\n在 Zeabur 项目页面：")
    print("1. 点击 'Add Service' 或 '+' 按钮")
    print("2. 选择 'Database' → 'PostgreSQL'")
    print("3. Zeabur 会自动设置 DATABASE_URL")
    
    print_step(4, "配置环境变量")
    show_env_vars_guide()
    
    if has_cli:
        print_step(5, "使用 Zeabur CLI")
        print("\n✅ Zeabur CLI 已安装，可以使用以下命令：")
        show_zeabur_commands()
        
        print("\n是否现在执行 Zeabur CLI 命令？")
        print("1. 登录 Zeabur")
        print("2. 链接项目")
        print("3. 运行数据库迁移")
        print("4. 跳过（稍后手动执行）")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n执行: zeabur login")
            subprocess.run(["zeabur", "login"])
        elif choice == "2":
            print("\n执行: zeabur link")
            subprocess.run(["zeabur", "link"])
        elif choice == "3":
            print("\n执行: zeabur exec alembic upgrade head")
            subprocess.run(["zeabur", "exec", "alembic", "upgrade", "head"])
    else:
        print_step(5, "安装 Zeabur CLI（可选）")
        print("\n要使用 Zeabur CLI，请先安装：")
        print("  npm i -g @zeabur/cli")
        print("\n然后可以使用命令行工具管理部署")
    
    print("\n" + "=" * 60)
    print("部署检查清单")
    print("=" * 60)
    print("\n请确认以下步骤：")
    print("[ ] 项目已在 Zeabur 创建")
    print("[ ] PostgreSQL 数据库已添加")
    print("[ ] 所有环境变量已配置")
    print("[ ] 数据库迁移已运行")
    print("[ ] 服务正常运行")
    print("[ ] 获取了域名")
    print("[ ] Facebook Webhook 已配置")
    
    print("\n" + "=" * 60)
    print("详细步骤请查看: ZEABUR_DEPLOY_NOW.md")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)


