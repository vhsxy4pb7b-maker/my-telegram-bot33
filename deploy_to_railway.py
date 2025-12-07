"""Railway 部署辅助脚本"""
import sys
import subprocess
from typing import Optional, Tuple


# 常量定义
SEPARATOR = "=" * 60
REPO_NAME = "vhsxy4pb7b-maker/my-telegram-bot33"
RAILWAY_URL = "https://railway.app"

# 环境变量配置
ENV_VARS = [
    ("FACEBOOK_APP_ID", "你的Facebook应用ID"),
    ("FACEBOOK_APP_SECRET", "你的Facebook应用密钥"),
    ("FACEBOOK_ACCESS_TOKEN", "你的Facebook访问令牌"),
    ("FACEBOOK_VERIFY_TOKEN", "你的Facebook验证令牌（自定义字符串）"),
    ("OPENAI_API_KEY", "你的OpenAI API密钥"),
    ("TELEGRAM_BOT_TOKEN", "你的Telegram Bot令牌"),
    ("TELEGRAM_CHAT_ID", "你的Telegram聊天ID"),
    ("SECRET_KEY", "YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U（已生成）"),
]

# Railway CLI 命令
RAILWAY_COMMANDS = {
    "1": ("登录 Railway", ["railway", "login"]),
    "2": ("链接项目", ["railway", "link"]),
    "3": ("运行数据库迁移", ["railway", "run", "alembic", "upgrade", "head"]),
}


def print_step(step_num: int, title: str) -> None:
    """打印步骤标题"""
    print(f"\n{SEPARATOR}")
    print(f"步骤 {step_num}: {title}")
    print(SEPARATOR)


def check_railway_cli() -> bool:
    """检查 Railway CLI 是否安装"""
    try:
        result = subprocess.run(
            ["railway", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print("✅ Railway CLI 已安装")
            return True
    except FileNotFoundError:
        pass

    print("❌ Railway CLI 未安装")
    print("\n安装命令:")
    print("  npm i -g @railway/cli")
    return False


def check_git_status() -> bool:
    """检查 Git 状态"""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            check=False
        )
        if "railway" in result.stdout.lower() or "github.com" in result.stdout.lower():
            print("✅ Git 远程仓库已配置")
            return True
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    print("⚠️  Git 远程仓库未配置或未检测到")
    return False


def show_env_vars_guide() -> None:
    """显示环境变量配置指南"""
    print(f"\n{SEPARATOR}")
    print("环境变量配置指南")
    print(SEPARATOR)
    print("\n请在 Railway 项目页面 → Variables 中添加以下变量：\n")

    for var, desc in ENV_VARS:
        print(f"  {var:30} = {desc}")

    print("\n注意: DATABASE_URL 由 Railway 自动设置，无需手动添加")


def show_railway_commands() -> None:
    """显示 Railway CLI 命令"""
    print(f"\n{SEPARATOR}")
    print("Railway CLI 常用命令")
    print(SEPARATOR)
    print("\n1. 登录 Railway:")
    print("   railway login")
    print("\n2. 链接项目:")
    print("   railway link")
    print("\n3. 运行数据库迁移:")
    print("   railway run alembic upgrade head")
    print("\n4. 查看日志:")
    print("   railway logs")
    print("\n5. 查看变量:")
    print("   railway variables")


def execute_railway_command(choice: str) -> None:
    """执行 Railway CLI 命令"""
    if choice in RAILWAY_COMMANDS:
        desc, cmd = RAILWAY_COMMANDS[choice]
        print(f"\n执行: {desc}")
        subprocess.run(cmd, check=False)


def show_deployment_steps() -> None:
    """显示部署步骤"""
    print_step(2, "部署步骤")
    print("\n由于 Railway 部署需要在网页上操作，请按照以下步骤：")
    print(f"\n1. 访问 {RAILWAY_URL}")
    print("2. 登录（使用 GitHub 账号）")
    print("3. 点击 'New Project'")
    print("4. 选择 'Deploy from GitHub repo'")
    print(f"5. 选择仓库: {REPO_NAME}")
    print("6. 等待部署开始")


def show_database_setup() -> None:
    """显示数据库设置步骤"""
    print_step(3, "添加数据库")
    print("\n在 Railway 项目页面：")
    print("1. 点击 'New' 按钮")
    print("2. 选择 'Database' → 'Add PostgreSQL'")
    print("3. Railway 会自动设置 DATABASE_URL")


def show_deployment_checklist() -> None:
    """显示部署检查清单"""
    print(f"\n{SEPARATOR}")
    print("部署检查清单")
    print(SEPARATOR)
    print("\n请确认以下步骤：")
    checklist_items = [
        "项目已在 Railway 创建",
        "PostgreSQL 数据库已添加",
        "所有环境变量已配置",
        "数据库迁移已运行",
        "服务正常运行",
        "获取了 Public Domain",
        "Facebook Webhook 已配置",
    ]
    for item in checklist_items:
        print(f"[ ] {item}")


def handle_railway_cli_interaction(has_cli: bool) -> None:
    """处理 Railway CLI 交互"""
    if has_cli:
        print_step(5, "使用 Railway CLI")
        print("\n✅ Railway CLI 已安装，可以使用以下命令：")
        show_railway_commands()

        print("\n是否现在执行 Railway CLI 命令？")
        print("1. 登录 Railway")
        print("2. 链接项目")
        print("3. 运行数据库迁移")
        print("4. 跳过（稍后手动执行）")

        choice = input("\n请选择 (1-4): ").strip()

        if choice != "4":
            execute_railway_command(choice)
    else:
        print_step(5, "安装 Railway CLI（可选）")
        print("\n要使用 Railway CLI，请先安装：")
        print("  npm i -g @railway/cli")
        print("\n然后可以使用命令行工具管理部署")


def main() -> None:
    """主函数"""
    print(f"\n{SEPARATOR}")
    print("Railway 部署辅助工具")
    print(SEPARATOR)

    # 检查环境
    print_step(1, "检查环境")
    has_cli = check_railway_cli()
    check_git_status()

    # 显示部署步骤
    show_deployment_steps()
    show_database_setup()

    # 配置环境变量
    print_step(4, "配置环境变量")
    show_env_vars_guide()

    # Railway CLI 交互
    handle_railway_cli_interaction(has_cli)

    # 显示检查清单
    show_deployment_checklist()

    print(f"\n{SEPARATOR}")
    print("详细步骤请查看: STEP_BY_STEP_RAILWAY.md")
    print(SEPARATOR)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
