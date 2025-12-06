"""检查 OAuth 授权状态"""
import os
import sys
from pathlib import Path


def check_env_file():
    """检查 .env 文件中的访问令牌"""
    env_path = Path(".env")

    if not env_path.exists():
        print("✗ .env 文件不存在")
        return False, None

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找访问令牌
        lines = content.split('\n')
        access_token = None

        for line in lines:
            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                access_token = line.split('=', 1)[1].strip()
                if access_token and not access_token.startswith('your_'):
                    return True, access_token

        if 'FACEBOOK_ACCESS_TOKEN' in content:
            print("⚠ .env 中有 FACEBOOK_ACCESS_TOKEN，但可能未配置")
        else:
            print("✗ .env 中未找到 FACEBOOK_ACCESS_TOKEN")

        return False, None

    except Exception as e:
        print(f"✗ 读取 .env 文件失败: {e}")
        return False, None


def check_token_validity(token):
    """检查访问令牌是否有效"""
    if not token:
        return False, "令牌为空"

    # 基本格式检查
    if len(token) < 50:
        return False, "令牌长度异常"

    if not (token.startswith('EAAB') or token.startswith('EAA')):
        return False, "令牌格式异常（应以 EAAB 或 EAA 开头）"

    # 尝试调用 Facebook API 验证
    try:
        import requests
        url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return True, f"令牌有效 - 用户: {data.get('name', 'N/A')}"
        elif response.status_code == 401:
            return False, "令牌无效或已过期"
        else:
            return False, f"API 返回错误: {response.status_code}"

    except ImportError:
        return None, "requests 库未安装，无法验证令牌"
    except Exception as e:
        return None, f"验证失败: {e}"


def check_service_running():
    """检查服务是否运行"""
    try:
        import requests
        response = requests.get(
            "http://localhost:8000/oauth/callback", timeout=2)
        return True
    except:
        return False


def main():
    print("=" * 60)
    print("  OAuth 授权状态检查")
    print("=" * 60)
    print()

    # 1. 检查 .env 文件
    print("1. 检查 .env 文件...")
    has_token, token = check_env_file()

    if has_token:
        print(f"   ✓ 找到访问令牌: {token[:20]}...{token[-10:]}")
        print()

        # 2. 验证令牌
        print("2. 验证访问令牌...")
        is_valid, message = check_token_validity(token)

        if is_valid is True:
            print(f"   ✓ {message}")
            print()
            print("=" * 60)
            print("  ✅ 授权成功！访问令牌已配置且有效")
            print("=" * 60)
            return True
        elif is_valid is False:
            print(f"   ✗ {message}")
            print()
            print("=" * 60)
            print("  ⚠ 访问令牌已配置，但无效或已过期")
            print("  建议重新授权获取新令牌")
            print("=" * 60)
            return False
        else:
            print(f"   ⚠ {message}")
            print("   （无法验证，但令牌格式正确）")
    else:
        print("   ✗ 未找到访问令牌")
        print()
        print("=" * 60)
        print("  ⏳ 授权尚未完成")
        print("=" * 60)
        print()
        print("下一步操作：")
        print("1. 在浏览器中完成授权")
        print("2. 获取重定向 URL 中的 access_token")
        print("3. 运行: python extract_token.py \"重定向URL\"")
        return False

    # 3. 检查服务
    print()
    print("3. 检查服务状态...")
    if check_service_running():
        print("   ✓ 回调服务正在运行")
    else:
        print("   ⚠ 回调服务未运行（可选）")

    print()


if __name__ == "__main__":
    main()
