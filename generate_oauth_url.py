"""快速生成 Facebook OAuth 授权 URL"""
import urllib.parse
import sys


def generate_url(app_id, redirect_uri="http://localhost:8000/oauth/callback", scope="pages_messaging,pages_manage_metadata"):
    """生成 OAuth 授权 URL"""
    base_url = "https://www.facebook.com/v18.0/dialog/oauth"

    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "token"
    }

    query_string = urllib.parse.urlencode(params)
    auth_url = f"{base_url}?{query_string}"

    return auth_url


if __name__ == "__main__":
    print("=" * 60)
    print("Facebook OAuth 授权 URL 生成器")
    print("=" * 60)

    if len(sys.argv) > 1:
        app_id = sys.argv[1]
    else:
        app_id = input("\n请输入 Facebook App ID: ").strip()

    if not app_id:
        print("✗ App ID 不能为空")
        sys.exit(1)

    redirect_uri = input(
        "重定向 URI [http://localhost:8000/oauth/callback]: ").strip()
    if not redirect_uri:
        redirect_uri = "http://localhost:8000/oauth/callback"

    auth_url = generate_url(app_id, redirect_uri)

    print("\n" + "=" * 60)
    print("生成的授权 URL:")
    print("=" * 60)
    print(f"\n{auth_url}\n")
    print("=" * 60)

    print("\n下一步：")
    print("1. 复制上面的 URL")
    print("2. 在浏览器中打开")
    print("3. 登录并授权")
    print("4. 从重定向 URL 中提取 access_token")
    print("\n详细说明请查看: FACEBOOK_OAUTH_GUIDE.md")
