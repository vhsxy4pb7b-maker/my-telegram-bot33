"""交互式数据库设置 - 更友好的提示"""
import psycopg2
from psycopg2 import sql
import sys
import os


def create_database():
    """创建数据库 - 交互式版本"""

    print("=" * 60)
    print("PostgreSQL 数据库设置向导")
    print("=" * 60)

    print("\n本工具将帮助您：")
    print("1. 测试 PostgreSQL 连接")
    print("2. 创建数据库 'facebook_customer_service'")
    print("3. 自动更新 .env 文件中的 DATABASE_URL")

    print("\n" + "-" * 60)
    print("提示：如果还没有安装 PostgreSQL，请先安装")
    print("查看安装指南: QUICK_DB_SETUP.md")
    print("-" * 60)

    input("\n按回车键继续，或按 Ctrl+C 退出...")

    # 获取连接信息
    print("\n请输入 PostgreSQL 连接信息：")
    print("（直接按回车使用默认值）\n")

    host = input("主机地址 [localhost]: ").strip() or "localhost"
    port = input("端口 [5432]: ").strip() or "5432"
    user = input("用户名 [postgres]: ").strip() or "postgres"

    print("\n请输入 postgres 用户的密码：")
    print("（这是安装 PostgreSQL 时设置的密码）")
    password = input("密码: ").strip()

    if not password:
        print("\n✗ 密码不能为空")
        print("\n如果您忘记了密码，可以：")
        print("1. 重置 PostgreSQL 密码")
        print("2. 或使用其他有权限的用户")
        return False

    database_name = "facebook_customer_service"

    try:
        print(f"\n正在连接到 PostgreSQL ({host}:{port})...")
        print("请稍候...")

        conn = psycopg2.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database="postgres"
        )
        print("✓ 连接成功！")

        conn.autocommit = True
        cursor = conn.cursor()

        # 检查数据库是否已存在
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )

        if cursor.fetchone():
            print(f"\n⚠️  数据库 '{database_name}' 已存在")
            response = input("是否删除并重新创建？(y/N): ").strip().lower()
            if response == 'y':
                # 断开其他连接
                try:
                    cursor.execute(
                        f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{database_name}' AND pid <> pg_backend_pid()"
                    )
                except:
                    pass

                cursor.execute(
                    sql.SQL("DROP DATABASE {}").format(
                        sql.Identifier(database_name)
                    )
                )
                print(f"✓ 已删除旧数据库")
            else:
                print("使用现有数据库")
                cursor.close()
                conn.close()
                # 仍然更新 .env
                database_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
                update_env_file(database_url)
                return True

        # 创建数据库
        print(f"\n正在创建数据库 '{database_name}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(database_name)
            )
        )
        print(f"✓ 数据库 '{database_name}' 创建成功！")

        # 生成并更新 DATABASE_URL
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        update_env_file(database_url)

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("✓ 数据库设置完成！")
        print("=" * 60)
        print("\n下一步：")
        print("1. 初始化数据库表: alembic upgrade head")
        print("2. 验证配置: python verify_setup.py")
        print("3. 启动服务: python run.py")

        return True

    except psycopg2.OperationalError as e:
        error_msg = str(e)
        print(f"\n✗ 连接失败")

        if "Connection refused" in error_msg or "could not connect" in error_msg.lower():
            print("\n可能的原因：")
            print("1. PostgreSQL 服务未运行")
            print("2. 主机或端口不正确")
            print("\n解决方案：")
            print("- Windows: 打开服务管理器，查找 PostgreSQL 服务并启动")
            print("- 或运行: net start postgresql-x64-XX (XX 是版本号)")
        elif "password authentication failed" in error_msg.lower():
            print("\n可能的原因：")
            print("1. 密码不正确")
            print("2. 用户名不正确")
            print("\n解决方案：")
            print("- 确认安装 PostgreSQL 时设置的密码")
            print("- 或使用其他有权限的用户")
        else:
            print(f"\n错误详情: {error_msg}")

        print("\n需要帮助？查看: QUICK_DB_SETUP.md")
        return False
    except ImportError:
        print("\n✗ psycopg2 未安装")
        print("请运行: python -m pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        return False


def update_env_file(database_url):
    """更新 .env 文件中的 DATABASE_URL"""
    env_file = ".env"

    if not os.path.exists(env_file):
        print(f"\n⚠️  .env 文件不存在，创建新文件...")
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"DATABASE_URL={database_url}\n")
        print(f"✓ 已创建 .env 文件")
        return

    # 读取并更新
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("DATABASE_URL="):
            new_lines.append(f"DATABASE_URL={database_url}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"\nDATABASE_URL={database_url}\n")

    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✓ DATABASE_URL 已自动更新到 .env 文件")
    print(f"  连接字符串: postgresql://***:***@{database_url.split('@')[1]}")


if __name__ == "__main__":
    try:
        success = create_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n已取消操作")
        sys.exit(1)
