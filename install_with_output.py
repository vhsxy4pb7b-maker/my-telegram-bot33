"""带详细输出的依赖安装脚本"""
import importlib
import subprocess
import sys


def install_package(package):
    """安装单个包并显示输出"""
    print(f"\n{'='*60}")
    print(f"正在安装: {package}")
    print('='*60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "-v"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print(f"✓ {package} 安装成功")
            if result.stdout:
                print("输出:", result.stdout[-500:])  # 只显示最后500字符
            return True
        else:
            print(f"✗ {package} 安装失败")
            print("错误输出:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {package} 安装超时")
        return False
    except Exception as e:
        print(f"✗ {package} 安装异常: {str(e)}")
        return False


# 核心包列表
core_packages = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
]

print("开始安装核心依赖包...")
print("这可能需要几分钟时间，请耐心等待...\n")

success_count = 0
for package in core_packages:
    if install_package(package):
        success_count += 1

print(f"\n{'='*60}")
print(f"安装完成: {success_count}/{len(core_packages)} 成功")
print('='*60)

# 验证安装
print("\n验证安装...")
for package_name in ["fastapi", "uvicorn", "pydantic", "pydantic_settings"]:
    try:
        importlib.import_module(package_name)
        print(f"✓ {package_name}")
    except ImportError:
        print(f"✗ {package_name}")

