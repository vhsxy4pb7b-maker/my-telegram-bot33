"""快速配置 OpenAI API Key"""
import os
import sys

def update_env_file(key, value):
    """更新 .env 文件中的值"""
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
        return True
    
    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f"{key}={value}\n")
    
    with open(".env", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    return True

def main():
    print("=" * 60)
    print("快速配置 OpenAI API Key")
    print("=" * 60)
    
    print("\n📋 获取 OpenAI API Key:")
    print("1. 访问: https://platform.openai.com/api-keys")
    print("2. 登录或注册 OpenAI 账号")
    print("3. 点击 'Create new secret key'")
    print("4. 复制生成的密钥（只显示一次，请妥善保存）")
    print("\n" + "=" * 60)
    
    # 从命令行参数读取
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1].strip()
        print(f"\n✓ 从命令行参数读取 API Key: {api_key[:10]}...")
    else:
        api_key = input("\n请输入 OpenAI API Key: ").strip()
    
    if not api_key:
        print("✗ API Key 不能为空")
        return
    
    if not api_key.startswith("sk-"):
        print("⚠️  警告: OpenAI API Key 通常以 'sk-' 开头")
        confirm = input("是否继续? (y/N): ").strip().lower()
        if confirm != 'y':
            return
    
    # 保存到 .env
    print("\n正在保存到 .env 文件...")
    if update_env_file("OPENAI_API_KEY", api_key):
        print("✓ OpenAI API Key 已保存到 .env 文件")
    
    print("\n" + "=" * 60)
    print("✅ 配置完成！")
    print("=" * 60)
    print("\n运行以下命令验证配置:")
    print("  python verify_setup.py")
    print("\n或测试 AI 功能:")
    print("  python test_complete_flow.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")

