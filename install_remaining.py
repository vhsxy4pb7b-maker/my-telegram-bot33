"""安装剩余依赖包 - 显示完整输出"""
import subprocess
import sys

packages = ["sqlalchemy", "openai", "psycopg2-binary"]

print("=" * 60)
print("安装剩余依赖包")
print("=" * 60)
print(f"Python: {sys.executable}")
print(f"pip: {subprocess.check_output([sys.executable, '-m', 'pip', '--version']).decode().strip()}")
print("=" * 60)
print()

for package in packages:
    print(f"\n{'='*60}")
    print(f"正在安装: {package}")
    print('='*60)
    
    cmd = [
        sys.executable,
        "-m", "pip", "install",
        package,
        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
        "--no-cache-dir",
        "--upgrade"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    print()
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时输出
        for line in process.stdout:
            print(line, end='')
            if 'Successfully installed' in line or 'Requirement already satisfied' in line:
                break
        
        process.wait()
        
        if process.returncode == 0:
            print(f"\n✓ {package} 安装完成")
            
            # 验证
            if package == "psycopg2-binary":
                try:
                    __import__("psycopg2")
                    print(f"  ✓ {package} 验证成功")
                except ImportError:
                    print(f"  ✗ {package} 验证失败")
            else:
                try:
                    __import__(package)
                    print(f"  ✓ {package} 验证成功")
                except ImportError:
                    print(f"  ✗ {package} 验证失败")
        else:
            print(f"\n✗ {package} 安装失败 (返回码: {process.returncode})")
            
    except Exception as e:
        print(f"✗ {package} 安装异常: {e}")

print("\n" + "=" * 60)
print("最终验证")
print("=" * 60)

test_packages = {
    "sqlalchemy": "sqlalchemy",
    "openai": "openai",
    "psycopg2": "psycopg2",
}

all_ok = True
for display_name, module_name in test_packages.items():
    try:
        __import__(module_name)
        print(f"✓ {display_name}")
    except ImportError:
        print(f"✗ {display_name} - 未安装")
        all_ok = False

if all_ok:
    print("\n🎉 所有剩余依赖包安装成功！")
else:
    print("\n⚠️ 仍有部分包未安装成功")

