"""快速生成 Facebook OAuth 授权 URL"""
import urllib.parse
import sys


def generate_url(
    app_id, 
    redirect_uri="http://localhost:8000/oauth/callback", 
    scope="pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management"
):
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
    
    print("\n权限范围选项:")
    print("1. 基础权限（消息功能）")
    print("2. 基础 + 帖子管理")
    print("3. 基础 + 广告管理")
    print("4. 全部权限（推荐）")
    
    choice = input("\n请选择 [1-4，默认4]: ").strip()
    
    if choice == "1":
        scope = "pages_messaging,pages_read_engagement,pages_manage_metadata"
    elif choice == "2":
        scope = "pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts"
    elif choice == "3":
        scope = "pages_messaging,pages_read_engagement,pages_manage_metadata,ads_read,ads_management"
    else:
        scope = "pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management"
    
    print(f"\n使用的权限范围: {scope}")

    auth_url = generate_url(app_id, redirect_uri, scope)

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
