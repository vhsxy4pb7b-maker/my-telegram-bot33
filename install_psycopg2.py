"""专门安装 psycopg2-binary 的脚本"""
import subprocess
import sys

print("尝试安装 psycopg2-binary...")
print("=" * 60)

# 方法1: 使用 pip 安装
print("\n方法 1: 使用 pip 安装 psycopg2-binary")
cmd1 = [sys.executable, "-m", "pip", "install", "psycopg2-binary",
        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
        "--no-cache-dir"]

try:
    result = subprocess.run(cmd1, capture_output=True, text=True, timeout=300)
    print(f"返回码: {result.returncode}")
    if result.stdout:
        print("输出:")
        print(result.stdout[-1000:])  # 最后1000字符
    if result.stderr:
        print("错误:")
        print(result.stderr[-500:])
except Exception as e:
    print(f"异常: {e}")

# 验证
print("\n验证安装...")
try:
    import psycopg2
    print("✓ psycopg2 安装成功！")
    print(
        f"版本信息: {psycopg2.__version__ if hasattr(psycopg2, '__version__') else 'N/A'}")
except ImportError as e:
    print(f"✗ psycopg2 未安装: {e}")
    print("\n如果安装失败，可能需要:")
    print("1. 安装 Visual C++ Build Tools")
    print("2. 或使用 PostgreSQL 客户端库")
    print("3. 或暂时跳过，使用 SQLite 进行测试")
