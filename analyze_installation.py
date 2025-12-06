"""分析已安装的包并安装缺失的依赖"""
import subprocess
import sys

# 必需的包
required_packages = {
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn[standard]',
    'sqlalchemy': 'sqlalchemy',
    'alembic': 'alembic',
    'openai': 'openai',
    'yaml': 'pyyaml',
    'dotenv': 'python-dotenv',
    'psycopg2': 'psycopg2-binary',
    'aiohttp': 'aiohttp',
    'email_validator': 'email-validator',
}

print("=" * 60)
print("依赖包安装状态分析")
print("=" * 60)

# 检查已安装的包
installed = {}
missing = {}

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        installed[package_name] = True
        print(f"✓ {package_name} - 已安装")
    except ImportError:
        missing[package_name] = True
        print(f"✗ {package_name} - 未安装")

print("\n" + "=" * 60)
print(f"已安装: {len(installed)}/{len(required_packages)}")
print(f"缺失: {len(missing)}/{len(required_packages)}")
print("=" * 60)

if missing:
    print("\n开始安装缺失的包...")
    print("使用清华镜像源，这可能需要几分钟...\n")
    
    packages_to_install = list(missing.keys())
    install_cmd = [
        sys.executable, "-m", "pip", "install",
        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
        "--no-cache-dir"
    ] + packages_to_install
    
    print(f"执行命令: {' '.join(install_cmd)}\n")
    
    try:
        result = subprocess.run(
            install_cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ 安装完成！")
        if result.stdout:
            # 显示最后几行输出
            lines = result.stdout.strip().split('\n')
            print("\n安装输出（最后10行）:")
            for line in lines[-10:]:
                print(f"  {line}")
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装失败")
        print(f"错误: {e.stderr}")
    except Exception as e:
        print(f"✗ 安装异常: {str(e)}")
else:
    print("\n✓ 所有依赖包已安装！")

print("\n" + "=" * 60)
print("验证安装...")
print("=" * 60)

# 再次验证
all_installed = True
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"✓ {package_name}")
    except ImportError:
        print(f"✗ {package_name} - 仍然缺失")
        all_installed = False

if all_installed:
    print("\n🎉 所有依赖包安装成功！可以继续下一步配置了。")
else:
    print("\n⚠️ 仍有部分包未安装，请检查错误信息。")

