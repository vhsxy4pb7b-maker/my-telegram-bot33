"""将短期Token转换为长期Token"""
from src.config.page_token_manager import page_token_manager
from src.config import settings
import sys
import asyncio
import httpx
from pathlib import Path
from typing import Optional, Dict, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


async def exchange_for_long_lived_token(short_token: str, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    """
    将短期Token转换为长期Token

    Args:
        short_token: 短期Token
        app_id: Facebook App ID（可选，从环境变量读取）
        app_secret: Facebook App Secret（可选，从环境变量读取）

    Returns:
        长期Token，如果失败返回None
    """
    # 从环境变量或设置中获取App ID和Secret
    if not app_id:
        app_id = getattr(settings, 'facebook_app_id', None) or settings.facebook_access_token.split(
            '|')[0] if '|' in settings.facebook_access_token else None

    if not app_secret:
        app_secret = getattr(settings, 'facebook_app_secret', None)

    if not app_id or not app_secret:
        print("❌ 需要 Facebook App ID 和 App Secret")
        print("   请设置环境变量：")
        print("   - FACEBOOK_APP_ID")
        print("   - FACEBOOK_APP_SECRET")
        return None

    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                long_token = data.get("access_token")
                expires_in = data.get("expires_in", 0)

                # 计算过期时间
                from datetime import datetime, timezone, timedelta
                if expires_in > 0:
                    expires_days = expires_in // 86400  # 转换为天数
                    expires_at = datetime.now(
                        timezone.utc) + timedelta(seconds=expires_in)
                    expires_at_str = expires_at.isoformat()
                    print(f"✅ 成功获取长期Token")
                    print(f"   有效期：{expires_days} 天 ({expires_in} 秒)")
                    print(
                        f"   过期时间：{expires_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                else:
                    # expires_in 为 0 表示Token不会过期（永久Token）
                    expires_at_str = None
                    print(f"✅ 成功获取Token")
                    print(f"   有效期：永久（不会过期）")

                return long_token, expires_at_str
            else:
                error_data = response.json() if response.content else {}
                error = error_data.get("error", {})
                error_message = error.get("message", "未知错误")
                error_code = error.get("code", "未知")

                print(f"❌ 获取长期Token失败")
                print(f"   错误代码：{error_code}")
                print(f"   错误消息：{error_message}")
                return None, None
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None, None


async def get_page_tokens_from_user_token(user_token: str) -> Dict[str, Dict[str, Any]]:
    """
    从用户Token获取所有页面的Token

    Args:
        user_token: 用户Token（长期Token）

    Returns:
        页面Token字典 {page_id: {token, name}}
    """
    # 先尝试获取用户ID
    try:
        url = "https://graph.facebook.com/v18.0/me"
        params = {"access_token": user_token, "fields": "id"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                # 如果 /me 失败，可能是页面Token，尝试使用用户ID端点
                print("⚠️  Token可能是页面Token，尝试其他方法...")
                # 直接返回空，让用户手动提供页面Token
                return {}
    except:
        pass

    # 尝试获取页面列表
    url = "https://graph.facebook.com/v18.0/me/accounts"
    params = {"access_token": user_token}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                pages = data.get("data", [])

                result = {}
                for page in pages:
                    page_id = page.get("id")
                    page_token = page.get("access_token")
                    page_name = page.get("name")

                    if page_id and page_token:
                        result[page_id] = {
                            "token": page_token,
                            "name": page_name
                        }

                return result
            else:
                error_data = response.json() if response.content else {}
                error = error_data.get("error", {})
                error_message = error.get("message", "未知错误")
                error_code = error.get("code", "未知")

                print(f"❌ 获取页面列表失败: {error_message} (code: {error_code})")

                # 如果是页面Token，提示用户手动更新
                if "Page" in error_message or error_code == 100:
                    print()
                    print("💡 提示：")
                    print("   当前Token可能是页面Token，无法获取其他页面列表")
                    print("   请手动为每个页面更新Token：")
                    print(
                        "   python scripts/tools/quick_update_page_token.py <页面ID> <新Token>")

                return {}
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return {}


async def convert_all_tokens_to_long_lived():
    """将所有Token转换为长期Token"""
    print("=" * 70)
    print("将Token转换为长期Token")
    print("=" * 70)
    print()

    # 获取App ID和Secret
    try:
        app_id = settings.facebook_app_id
        app_secret = settings.facebook_app_secret
    except Exception:
        app_id = None
        app_secret = None

    if not app_id or not app_secret:
        print("⚠️  未配置 Facebook App ID 和 App Secret")
        print()
        print("请设置环境变量（在 .env 文件中）：")
        print("  FACEBOOK_APP_ID=your_app_id")
        print("  FACEBOOK_APP_SECRET=your_app_secret")
        print()
        print("或者直接提供用户Token，系统将使用它获取页面Token：")
        user_token = input("请输入用户Token（短期或长期）: ").strip()

        if not user_token:
            print("❌ 未提供Token")
            return

        # 如果是短期Token，先转换为长期Token（需要App ID和Secret）
        expires_at_str = None
        if app_id and app_secret:
            print()
            print("转换Token为长期Token...")
            long_user_token, expires_at_str = await exchange_for_long_lived_token(user_token, app_id, app_secret)

            if not long_user_token:
                print("⚠️  无法转换为长期Token，将使用提供的Token")
                long_user_token = user_token
                expires_at_str = None
        else:
            print("⚠️  无法转换Token（缺少App ID和Secret），将直接使用提供的Token")
            long_user_token = user_token

        # 获取页面Token
        print()
        print("获取页面Token...")
        page_tokens = await get_page_tokens_from_user_token(long_user_token)

        if not page_tokens:
            print("❌ 无法获取页面Token")
            return

        # 更新所有页面Token
        print()
        print("更新页面Token...")
        for page_id, page_info in page_tokens.items():
            page_token = page_info["token"]
            page_name = page_info["name"]

            # 页面Token的过期时间与用户Token相同
            page_token_manager.set_token(
                page_id, page_token, page_name, expires_at=expires_at_str)
            print(f"✅ 已更新页面 {page_id} ({page_name}) 的Token" +
                  (f" (过期时间: {expires_at_str})" if expires_at_str else ""))

        print()
        print("=" * 70)
        print("✅ 所有页面Token已更新为长期Token")
        print("=" * 70)
        return

    # 如果有App ID和Secret，使用默认Token转换
    default_token = settings.facebook_access_token
    if default_token:
        print("转换默认Token为长期Token...")
        long_token, expires_at_str = await exchange_for_long_lived_token(default_token, app_id, app_secret)

        if long_token:
            # 更新默认Token
            page_token_manager.set_default_token(long_token)
            print("✅ 已更新默认Token为长期Token" +
                  (f" (过期时间: {expires_at_str})" if expires_at_str else ""))

            # 获取页面Token
            print()
            print("获取页面Token...")
            page_tokens = await get_page_tokens_from_user_token(long_token)

            if page_tokens:
                print()
                print("更新页面Token...")
                for page_id, page_info in page_tokens.items():
                    page_token = page_info["token"]
                    page_name = page_info["name"]

                    # 页面Token的过期时间与用户Token相同
                    page_token_manager.set_token(
                        page_id, page_token, page_name, expires_at=expires_at_str)
                    print(f"✅ 已更新页面 {page_id} ({page_name}) 的Token" +
                          (f" (过期时间: {expires_at_str})" if expires_at_str else ""))
            else:
                print("⚠️  无法获取页面Token，但默认Token已更新")
        else:
            print("❌ 无法转换默认Token")

        print()
        print("=" * 70)
        print("✅ Token转换完成")
        print("=" * 70)
    else:
        print("❌ 未配置默认Token")

if __name__ == "__main__":
    asyncio.run(convert_all_tokens_to_long_lived())
