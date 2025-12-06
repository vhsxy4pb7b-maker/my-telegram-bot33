"""安装依赖脚本"""
import subprocess
import sys

packages = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
    "sqlalchemy==2.0.23",
    "alembic==1.12.1",
    "psycopg2-binary==2.9.9",
    "openai==1.3.5",
    "python-telegram-bot==20.7",
    "pyyaml==6.0.1",
    "python-dotenv==1.0.0",
    "httpx==0.25.2",
    "aiohttp==3.9.1",
    "requests==2.31.0",
    "email-validator==2.1.0",
]

print("开始安装依赖包...")
print("=" * 50)

for package in packages:
    print(f"\n正在安装: {package}")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {package} 安装成功")
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败")
        print(f"错误: {e.stderr}")

print("\n" + "=" * 50)
print("依赖安装完成！")

# 验证安装
print("\n验证安装...")
try:
    import fastapi
    print("✓ fastapi")
except ImportError:
    print("✗ fastapi")

try:
    import uvicorn
    print("✓ uvicorn")
except ImportError:
    print("✗ uvicorn")

try:
    import sqlalchemy
    print("✓ sqlalchemy")
except ImportError:
    print("✗ sqlalchemy")

try:
    import pydantic
    print("✓ pydantic")
except ImportError:
    print("✗ pydantic")

try:
    import pydantic_settings
    print("✓ pydantic-settings")
except ImportError:
    print("✗ pydantic-settings")

try:
    import openai
    print("✓ openai")
except ImportError:
    print("✗ openai")
