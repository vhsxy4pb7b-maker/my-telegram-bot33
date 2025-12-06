"""Facebook 短期令牌交换长期令牌工具"""
import requests
import sys
import os
from typing import Optional, Tuple

# 尝试从配置加载，如果失败则手动读取
try:
    from src.config import settings
    USE_CONFIG = True
except ImportError:
    USE_CONFIG = False
    settings = None


def _read_env_value(key: str, default_placeholder: str = "") -> Optional[str]:
    """从.env文件读取配置值"""
    if not os.path.exists(".env"):
        return None
    
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    value = line.split("=", 1)[1].strip()
                    if value and value != default_placeholder:
                        return value
    except (IOError, ValueError) as e:
        print(f"⚠️  读取 .env 文件时出错: {e}")
    
    return None


def exchange_token(
    short_token: Optional[str] = None,
    app_id: Optional[str] = None,
    app_secret: Optional[str] = None
) -> Optional[str]:
    """将短期访问令牌交换为长期访问令牌
    
    Args:
        short_token: 短期访问令牌
        app_id: Facebook App ID
        app_secret: Facebook App Secret
        
    Returns:
        长期访问令牌，如果交换失败则返回None
    """
    print("=" * 60)
    print("Facebook 访问令牌交换工具")
    print("=" * 60)

    # 获取参数
    if short_token is None:
        # 尝试从 .env 读取
        if USE_CONFIG:
            try:
                short_token = settings.facebook_access_token
                if short_token and short_token != "your_facebook_access_token":
                    print(
                        f"\n✓ 从 .env 读取短期令牌: {short_token[:20]}...{short_token[-10:]}")
                else:
                    short_token = None
            except:
                short_token = None

        if not short_token:
            short_token = _read_env_value("FACEBOOK_ACCESS_TOKEN", "your_facebook_access_token")
            if short_token:
                print(f"\n✓ 从 .env 读取短期令牌: {short_token[:20]}...{short_token[-10:]}")

        if not short_token:
            short_token = input("\n请输入短期访问令牌: ").strip()

    if app_id is None:
        if USE_CONFIG:
            try:
                app_id = settings.facebook_app_id
                if app_id and app_id != "your_facebook_app_id":
                    print(f"✓ 使用 App ID: {app_id}")
                else:
                    app_id = None
            except:
                app_id = None

        if not app_id:
            app_id = _read_env_value("FACEBOOK_APP_ID", "your_facebook_app_id")
            if app_id:
                print(f"✓ 使用 App ID: {app_id}")

        if not app_id:
            app_id = input("请输入 Facebook App ID: ").strip()

    if app_secret is None:
        if USE_CONFIG:
            try:
                app_secret = settings.facebook_app_secret
                if app_secret and app_secret != "your_facebook_app_secret":
                    print(f"✓ 使用 App Secret: {app_secret[:10]}...")
                else:
                    app_secret = None
            except:
                app_secret = None

        if not app_secret:
            app_secret = _read_env_value("FACEBOOK_APP_SECRET", "your_facebook_app_secret")
            if app_secret:
                print(f"✓ 使用 App Secret: {app_secret[:10]}...")

        if not app_secret:
            print("\n需要 Facebook App Secret 来交换长期令牌")
            print("获取方式: https://developers.facebook.com/apps/848496661333193/settings/basic/")
            app_secret = input("请输入 Facebook App Secret: ").strip()

    if not all([short_token, app_id, app_secret]):
        print("✗ 缺少必需参数")
        return None

    # 交换令牌
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }

    print("\n正在交换令牌...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            long_token = data["access_token"]
            expires_in = data.get("expires_in", "N/A")

            print("\n" + "=" * 60)
            print("✓ 令牌交换成功！")
            print("=" * 60)
            print(f"\n长期访问令牌: {long_token}")
            print(
                f"过期时间: {expires_in} 秒 ({int(expires_in) // 86400 if isinstance(expires_in, int) else 'N/A'} 天)")

            print("\n" + "=" * 60)
            print("下一步")
            print("=" * 60)
            print("\n请将以下内容添加到 .env 文件：")
            print(f"FACEBOOK_ACCESS_TOKEN={long_token}")

            # 询问是否自动更新
            update = input("\n是否自动更新到 .env 文件? (y/N): ").strip().lower()
            if update == 'y':
                try:
                    from configure_api_keys import update_env_file
                    if update_env_file("FACEBOOK_ACCESS_TOKEN", long_token):
                        print("✓ 已更新到 .env 文件")
                    else:
                        print("⚠️  更新 .env 文件失败，请手动更新")
                except ImportError:
                    print("⚠️  无法导入配置模块，请手动更新 .env 文件")
                except Exception as e:
                    print(f"⚠️  更新 .env 文件时出错: {e}")
                    print("请手动将以下内容添加到 .env 文件：")
                    print(f"FACEBOOK_ACCESS_TOKEN={long_token}")

            return long_token
        else:
            error_msg = data.get("error", {}).get("message", "未知错误")
            print(f"\n✗ 交换失败: {error_msg}")
            if "error" in data:
                print(f"错误详情: {data['error']}")
            return None

    except requests.exceptions.Timeout:
        print("\n✗ 请求超时，请检查网络连接后重试")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"响应内容: {e.response.text}")
        return None
    except Exception as e:
        print(f"\n✗ 发生未知错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    exchange_token()
