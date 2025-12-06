"""直接安装脚本 - 显示完整输出"""
import subprocess
import sys
import os

packages = [
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "openai",
    "pyyaml",
    "psycopg2-binary",
    "aiohttp",
    "email-validator",
]

print("=" * 60)
print("开始安装依赖包")
print("=" * 60)
print(f"Python: {sys.executable}")
print(f"pip: {subprocess.check_output([sys.executable, '-m', 'pip', '--version']).decode().strip()}")
print("=" * 60)
print()

for package in packages:
    print(f"\n正在安装: {package}")
    print("-" * 60)
    
    cmd = [
        sys.executable,
        "-m", "pip", "install",
        package,
        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
        "--no-cache-dir",
        "--upgrade"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(f"返回码: {result.returncode}")
        
        if result.stdout:
            # 显示关键信息
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['successfully', 'installed', 'requirement', 'already', 'error', 'warning']):
                    print(f"  {line}")
        
        if result.stderr:
            print("错误/警告:")
            for line in result.stderr.split('\n')[:10]:
                if line.strip():
                    print(f"  {line}")
        
        if result.returncode == 0:
            # 验证安装
            try:
                if package == "uvicorn[standard]":
                    __import__("uvicorn")
                    print(f"  ✓ {package} 安装并验证成功")
                elif package == "psycopg2-binary":
                    __import__("psycopg2")
                    print(f"  ✓ {package} 安装并验证成功")
                elif package == "pyyaml":
                    __import__("yaml")
                    print(f"  ✓ {package} 安装并验证成功")
                elif package == "email-validator":
                    __import__("email_validator")
                    print(f"  ✓ {package} 安装并验证成功")
                else:
                    module_name = package.split('[')[0]
                    __import__(module_name)
                    print(f"  ✓ {package} 安装并验证成功")
            except ImportError as e:
                print(f"  ✗ {package} 安装但验证失败: {e}")
        else:
            print(f"  ✗ {package} 安装失败")
            
    except subprocess.TimeoutExpired:
        print(f"  ✗ {package} 安装超时")
    except Exception as e:
        print(f"  ✗ {package} 安装异常: {e}")

print("\n" + "=" * 60)
print("最终验证")
print("=" * 60)

test_imports = {
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "sqlalchemy": "sqlalchemy",
    "openai": "openai",
    "yaml": "yaml",
    "psycopg2": "psycopg2",
    "aiohttp": "aiohttp",
    "email_validator": "email_validator",
}

all_ok = True
for display_name, module_name in test_imports.items():
    try:
        __import__(module_name)
        print(f"✓ {display_name}")
    except ImportError:
        print(f"✗ {display_name} - 未安装")
        all_ok = False

if all_ok:
    print("\n🎉 所有依赖包安装成功！")
else:
    print("\n⚠️ 仍有部分包未安装成功")

