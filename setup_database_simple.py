"""简化的数据库设置脚本 - 支持命令行参数"""
import psycopg2
from psycopg2 import sql
import sys
import os


def create_database(host="localhost", port="5432", user="postgres", password=None, database_name="facebook_customer_service"):
    """创建数据库"""

    print("=" * 60)
    print("PostgreSQL 数据库创建工具")
    print("=" * 60)

    if not password:
        print("\n使用方法：")
        print("  python setup_database_simple.py")
        print("  或设置环境变量：")
        print("  $env:PGPASSWORD='your_password'; python setup_database_simple.py")
        print("\n或使用命令行参数：")
        print("  python setup_database_simple.py --host localhost --port 5432 --user postgres --password your_password")
        return False

    try:
        print(f"\n正在连接到 PostgreSQL ({host}:{port})...")
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database="postgres"
        )
        print("✓ 连接成功")

        conn.autocommit = True
        cursor = conn.cursor()

        # 检查数据库是否已存在
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )

        if cursor.fetchone():
            print(f"✓ 数据库 '{database_name}' 已存在")
        else:
            # 创建数据库
            print(f"正在创建数据库 '{database_name}'...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )
            print(f"✓ 数据库 '{database_name}' 创建成功！")

        # 生成 DATABASE_URL
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

        # 更新 .env 文件
        env_file = ".env"
        if os.path.exists(env_file):
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
        else:
            print(f"\n数据库连接字符串：")
            print(f"DATABASE_URL={database_url}")
            print("请手动添加到 .env 文件")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("下一步：")
        print("1. 运行: alembic upgrade head")
        print("2. 运行: python verify_setup.py")
        print("=" * 60)

        return True

    except psycopg2.OperationalError as e:
        print(f"\n✗ 连接失败: {e}")
        print("\n可能的原因：")
        print("1. PostgreSQL 服务未运行")
        print("2. 主机、端口、用户名或密码不正确")
        print("3. PostgreSQL 未安装")
        print("\n解决方案：")
        print("- 检查 PostgreSQL 服务是否运行")
        print("- 查看 QUICK_DB_SETUP.md 了解安装步骤")
        return False
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        return False


if __name__ == "__main__":
    # 从命令行参数获取
    import argparse
    parser = argparse.ArgumentParser(description='创建 PostgreSQL 数据库')
    parser.add_argument('--host', default='localhost', help='数据库主机')
    parser.add_argument('--port', default='5432', help='数据库端口')
    parser.add_argument('--user', default='postgres', help='数据库用户')
    parser.add_argument('--password', default=None, help='数据库密码')
    parser.add_argument(
        '--database', default='facebook_customer_service', help='数据库名称')

    args = parser.parse_args()

    # 优先使用环境变量
    password = args.password or os.getenv('PGPASSWORD')

    success = create_database(
        host=args.host,
        port=args.port,
        user=args.user,
        password=password,
        database_name=args.database
    )

    sys.exit(0 if success else 1)
