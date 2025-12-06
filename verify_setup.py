"""配置验证脚本

运行此脚本来验证系统配置是否正确
"""
import sys
import os


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(
            f"✓ Python 版本: {version.major}.{version.minor}.{version.micro} (符合要求)")
        return True
    else:
        print(
            f"✗ Python 版本: {version.major}.{version.minor}.{version.micro} (需要 3.9+)")
        return False


def check_dependencies():
    """检查依赖是否安装"""
    # 包名到模块名的映射
    package_mapping = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'alembic': 'alembic',
        'pydantic': 'pydantic',
        'pydantic_settings': 'pydantic_settings',
        'openai': 'openai',
        'telegram': 'telegram',
        'pyyaml': 'yaml',  # PyYAML 包的模块名是 yaml
        'python_dotenv': 'dotenv',  # python-dotenv 包的模块名是 dotenv
        'httpx': 'httpx',
        'psycopg2': 'psycopg2'
    }

    missing = []
    for package_name, module_name in package_mapping.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            missing.append(package_name)

    if missing:
        print(f"\n缺少以下依赖，请运行: pip install {' '.join(missing)}")
        return False
    return True


def check_config_files():
    """检查配置文件是否存在"""
    files = {
        '.env': '环境变量配置文件',
        'config.yaml': '业务配置文件'
    }

    all_exist = True
    for file, desc in files.items():
        if os.path.exists(file):
            print(f"✓ {file} 存在 ({desc})")
        else:
            print(f"✗ {file} 不存在 ({desc})")
            all_exist = False

    return all_exist


def check_env_variables():
    """检查环境变量配置"""
    if not os.path.exists('.env'):
        print("✗ .env 文件不存在，无法检查环境变量")
        return False

    required_vars = [
        'DATABASE_URL',
        'FACEBOOK_APP_ID',
        'FACEBOOK_APP_SECRET',
        'FACEBOOK_ACCESS_TOKEN',
        'FACEBOOK_VERIFY_TOKEN',
        'OPENAI_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'SECRET_KEY'
    ]

    try:
        from dotenv import load_dotenv
        load_dotenv()

        missing = []
        for var in required_vars:
            value = os.getenv(var)
            if value and value not in ['your_', 'your-']:  # 检查是否是默认值
                print(f"✓ {var} 已配置")
            else:
                print(f"✗ {var} 未配置或使用默认值")
                missing.append(var)

        if missing:
            print(f"\n需要配置以下环境变量: {', '.join(missing)}")
            return False
        return True
    except ImportError:
        print("✗ python-dotenv 未安装，无法检查环境变量")
        return False


def check_database_connection():
    """检查数据库连接"""
    try:
        from src.config import settings
        from src.database.database import engine

        # 尝试连接数据库
        with engine.connect() as conn:
            print("✓ 数据库连接成功")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {str(e)}")
        print("  请检查 DATABASE_URL 配置和 PostgreSQL 服务是否运行")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("Facebook 客服自动化系统 - 配置验证")
    print("=" * 50)
    print()

    results = []

    print("1. 检查 Python 版本...")
    results.append(check_python_version())
    print()

    print("2. 检查依赖包...")
    results.append(check_dependencies())
    print()

    print("3. 检查配置文件...")
    results.append(check_config_files())
    print()

    print("4. 检查环境变量...")
    results.append(check_env_variables())
    print()

    print("5. 检查数据库连接...")
    results.append(check_database_connection())
    print()

    print("=" * 50)
    if all(results):
        print("✓ 所有检查通过！系统已准备就绪。")
        print("\n可以运行以下命令启动服务:")
        print("  python run.py")
    else:
        print("✗ 部分检查未通过，请根据上述提示修复问题。")
        print("\n参考文档:")
        print("  - START_HERE.md - 快速开始指南")
        print("  - CHECKLIST.md - 配置检查清单")
        print("  - API_KEYS_GUIDE.md - API 密钥获取指南")
    print("=" * 50)


if __name__ == "__main__":
    main()
