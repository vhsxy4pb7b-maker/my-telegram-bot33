"""创建数据库的辅助脚本"""
import psycopg2
from psycopg2 import sql
import sys


def create_database():
    """创建 facebook_customer_service 数据库"""

    print("=" * 60)
    print("PostgreSQL 数据库创建工具")
    print("=" * 60)

    # 获取连接信息
    print("\n请输入 PostgreSQL 连接信息：")
    host = input("主机 [localhost]: ").strip() or "localhost"
    port = input("端口 [5432]: ").strip() or "5432"
    user = input("用户名 [postgres]: ").strip() or "postgres"
    password = input("密码: ").strip()
    database_name = "facebook_customer_service"

    if not password:
        print("✗ 密码不能为空")
        return False

    try:
        # 连接到默认的 postgres 数据库
        print(f"\n正在连接到 PostgreSQL ({host}:{port})...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres"  # 连接到默认数据库
        )

        conn.autocommit = True
        cursor = conn.cursor()

        # 检查数据库是否已存在
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )

        if cursor.fetchone():
            print(f"⚠️  数据库 '{database_name}' 已存在")
            response = input("是否删除并重新创建？(y/N): ").strip().lower()
            if response == 'y':
                # 断开其他连接
                cursor.execute(
                    f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{database_name}' AND pid <> pg_backend_pid()"
                )
                cursor.execute(sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(database_name)
                ))
                print(f"✓ 已删除旧数据库")
            else:
                print("使用现有数据库")
                cursor.close()
                conn.close()
                return True

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
        print(f"\n数据库连接字符串：")
        print(f"DATABASE_URL={database_url}")
        print(f"\n请将此字符串复制到 .env 文件中")

        cursor.close()
        conn.close()
        return True

    except psycopg2.OperationalError as e:
        print(f"✗ 连接失败: {e}")
        print("\n请检查：")
        print("1. PostgreSQL 服务是否运行")
        print("2. 主机、端口、用户名、密码是否正确")
        return False
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


if __name__ == "__main__":
    success = create_database()
    if success:
        print("\n" + "=" * 60)
        print("下一步：")
        print("1. 将 DATABASE_URL 添加到 .env 文件")
        print("2. 运行: alembic upgrade head")
        print("3. 运行: python verify_setup.py")
        print("=" * 60)
    else:
        print("\n数据库创建失败，请检查错误信息")
        sys.exit(1)
