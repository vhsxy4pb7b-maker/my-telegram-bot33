"""检查 OpenAI API Key 配置"""
import os

def check_openai_key():
    """检查 OpenAI API Key 是否已配置"""
    if not os.path.exists(".env"):
        print("✗ .env 文件不存在")
        return False
    
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key and not key.startswith("your_"):
                    print(f"✓ OpenAI API Key 已配置: {key[:10]}...{key[-5:]}")
                    return True
                else:
                    print("⚠ OpenAI API Key 存在但未配置（为占位符）")
                    return False
    
    print("✗ OpenAI API Key 未配置")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("检查 OpenAI API Key 配置")
    print("=" * 60)
    print()
    check_openai_key()

