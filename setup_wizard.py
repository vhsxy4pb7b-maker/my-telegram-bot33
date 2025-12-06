"""配置向导 - 一步步完成系统配置"""
import os
import secrets
import sys


def print_step(step_num, title):
    """打印步骤标题"""
    print("\n" + "=" * 60)
    print(f"步骤 {step_num}: {title}")
    print("=" * 60)


def update_env_file(key, value, description):
    """更新 .env 文件中的值"""
    env_file = ".env"

    if not os.path.exists(env_file):
        print(f"✗ .env 文件不存在")
        return False

    # 读取文件
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 更新或添加配置
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
            print(f"✓ 已更新: {key}")
        else:
            new_lines.append(line)

    if not updated:
        # 如果不存在，添加到文件末尾
        new_lines.append(f"{key}={value}\n")
        print(f"✓ 已添加: {key}")

    # 写回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    return True


def step1_generate_secret_key():
    """步骤 1: 生成 SECRET_KEY"""
    print_step(1, "生成安全密钥 (SECRET_KEY)")

    secret_key = secrets.token_urlsafe(32)
    print(f"\n生成的 SECRET_KEY: {secret_key}")

    if update_env_file("SECRET_KEY", secret_key, "安全密钥"):
        print("✓ SECRET_KEY 已保存到 .env 文件")
        return True
    return False


def step2_configure_database():
    """步骤 2: 配置数据库"""
    print_step(2, "配置 PostgreSQL 数据库")

    print("\n请选择：")
    print("1. 已安装 PostgreSQL，直接配置连接")
    print("2. 需要安装 PostgreSQL（将提供安装指南）")
    print("3. 暂时跳过，稍后配置")

    choice = input("\n请选择 (1/2/3): ").strip()

    if choice == "1":
        print("\n请输入 PostgreSQL 连接信息：")
        host = input("主机 [localhost]: ").strip() or "localhost"
        port = input("端口 [5432]: ").strip() or "5432"
        user = input("用户名 [postgres]: ").strip() or "postgres"
        password = input("密码: ").strip()
        database = input("数据库名 [facebook_customer_service]: ").strip(
        ) or "facebook_customer_service"

        if not password:
            print("✗ 密码不能为空")
            return False

        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        # 测试连接
        print("\n正在测试数据库连接...")
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database="postgres"  # 先连接到默认数据库
            )
            conn.close()
            print("✓ 数据库连接成功")

            # 检查数据库是否存在
            try:
                conn = psycopg2.connect(
                    host=host,
                    port=int(port),
                    user=user,
                    password=password,
                    database=database
                )
                conn.close()
                print(f"✓ 数据库 '{database}' 已存在")
            except psycopg2.OperationalError:
                print(f"⚠️  数据库 '{database}' 不存在")
                create = input(
                    f"是否创建数据库 '{database}'? (y/N): ").strip().lower()
                if create == 'y':
                    try:
                        conn = psycopg2.connect(
                            host=host,
                            port=int(port),
                            user=user,
                            password=password,
                            database="postgres"
                        )
                        conn.autocommit = True
                        cursor = conn.cursor()
                        cursor.execute(f'CREATE DATABASE "{database}"')
                        cursor.close()
                        conn.close()
                        print(f"✓ 数据库 '{database}' 创建成功")
                    except Exception as e:
                        print(f"✗ 创建数据库失败: {e}")
                        return False

            if update_env_file("DATABASE_URL", database_url, "数据库连接字符串"):
                print("✓ DATABASE_URL 已保存到 .env 文件")
                return True
        except ImportError:
            print("✗ psycopg2 未安装，无法测试连接")
            print("  但已保存配置，请稍后验证")
            update_env_file("DATABASE_URL", database_url, "数据库连接字符串")
            return True
        except Exception as e:
            print(f"✗ 数据库连接失败: {e}")
            print("  配置已保存，但请检查连接信息")
            update_env_file("DATABASE_URL", database_url, "数据库连接字符串")
            return False

    elif choice == "2":
        print("\n" + "=" * 60)
        print("PostgreSQL 安装指南")
        print("=" * 60)
        print("\n1. 访问下载页面：")
        print("   https://www.postgresql.org/download/windows/")
        print("\n2. 或使用 EnterpriseDB 安装程序：")
        print("   https://www.enterprisedb.com/downloads/postgres-postgresql-downloads")
        print("\n3. 安装时请记住设置的 postgres 用户密码")
        print("\n4. 安装完成后，重新运行此脚本选择选项 1")
        print("\n详细说明请查看: SETUP_POSTGRESQL.md")
        return False

    else:
        print("已跳过数据库配置，稍后可以手动配置")
        return False


def step3_configure_facebook():
    """步骤 3: 配置 Facebook API"""
    print_step(3, "配置 Facebook API")

    print("\n需要从 Facebook Developer Console 获取以下信息：")
    print("参考: API_KEYS_GUIDE.md")
    print("\n1. 访问: https://developers.facebook.com/")
    print("2. 创建应用并获取 App ID 和 App Secret")
    print("3. 生成访问令牌")

    print("\n请输入 Facebook API 配置：")
    app_id = input("FACEBOOK_APP_ID [留空跳过]: ").strip()
    if app_id:
        update_env_file("FACEBOOK_APP_ID", app_id, "Facebook 应用 ID")

    app_secret = input("FACEBOOK_APP_SECRET [留空跳过]: ").strip()
    if app_secret:
        update_env_file("FACEBOOK_APP_SECRET", app_secret, "Facebook 应用密钥")

    access_token = input("FACEBOOK_ACCESS_TOKEN [留空跳过]: ").strip()
    if access_token:
        update_env_file("FACEBOOK_ACCESS_TOKEN", access_token, "Facebook 访问令牌")

    verify_token = input("FACEBOOK_VERIFY_TOKEN [留空使用默认]: ").strip()
    if not verify_token:
        verify_token = secrets.token_urlsafe(16)
        print(f"使用自动生成的验证令牌: {verify_token}")
    update_env_file("FACEBOOK_VERIFY_TOKEN",
                    verify_token, "Facebook Webhook 验证令牌")

    if app_id and app_secret:
        print("✓ Facebook API 配置完成")
        return True
    else:
        print("⚠️  Facebook API 配置不完整，请稍后补充")
        return False


def step4_configure_openai():
    """步骤 4: 配置 OpenAI API"""
    print_step(4, "配置 OpenAI API")

    print("\n需要从 OpenAI Platform 获取 API 密钥：")
    print("1. 访问: https://platform.openai.com/api-keys")
    print("2. 登录并创建新的 API 密钥")

    api_key = input("\nOPENAI_API_KEY [留空跳过]: ").strip()
    if api_key:
        update_env_file("OPENAI_API_KEY", api_key, "OpenAI API 密钥")
        print("✓ OpenAI API 配置完成")
        return True
    else:
        print("⚠️  已跳过，请稍后配置")
        return False


def step5_configure_telegram():
    """步骤 5: 配置 Telegram Bot"""
    print_step(5, "配置 Telegram Bot")

    print("\n需要创建 Telegram Bot：")
    print("1. 在 Telegram 中搜索 @BotFather")
    print("2. 发送 /newbot 命令创建 Bot")
    print("3. 复制返回的 Bot Token")

    bot_token = input("\nTELEGRAM_BOT_TOKEN [留空跳过]: ").strip()
    if bot_token:
        update_env_file("TELEGRAM_BOT_TOKEN", bot_token, "Telegram Bot Token")

    chat_id = input("TELEGRAM_CHAT_ID [留空跳过]: ").strip()
    if chat_id:
        update_env_file("TELEGRAM_CHAT_ID", chat_id, "Telegram Chat ID")

    if bot_token and chat_id:
        print("✓ Telegram Bot 配置完成")
        return True
    else:
        print("⚠️  Telegram Bot 配置不完整，请稍后补充")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook 客服自动化系统 - 配置向导")
    print("=" * 60)
    print("\n本向导将帮助您一步步完成系统配置")
    print("您可以随时按 Ctrl+C 退出，稍后继续")

    steps_completed = []

    try:
        # 步骤 1: 生成 SECRET_KEY
        if step1_generate_secret_key():
            steps_completed.append("SECRET_KEY")

        # 步骤 2: 配置数据库
        if step2_configure_database():
            steps_completed.append("数据库")

        # 步骤 3: 配置 Facebook
        if step3_configure_facebook():
            steps_completed.append("Facebook API")

        # 步骤 4: 配置 OpenAI
        if step4_configure_openai():
            steps_completed.append("OpenAI API")

        # 步骤 5: 配置 Telegram
        if step5_configure_telegram():
            steps_completed.append("Telegram Bot")

        # 总结
        print("\n" + "=" * 60)
        print("配置完成总结")
        print("=" * 60)
        print(
            f"\n已完成的配置: {', '.join(steps_completed) if steps_completed else '无'}")

        print("\n下一步：")
        print("1. 运行验证: python verify_setup.py")
        if "数据库" in steps_completed:
            print("2. 初始化数据库: alembic upgrade head")
        print("3. 启动服务: python run.py")

    except KeyboardInterrupt:
        print("\n\n配置已中断，已完成的配置已保存")
        print("可以稍后继续运行此脚本完成剩余配置")


if __name__ == "__main__":
    main()
