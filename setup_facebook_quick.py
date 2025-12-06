"""Facebook OAuth 快速设置 - 支持命令行参数"""
import urllib.parse
import webbrowser
import sys
import os


def generate_auth_url(app_id, redirect_uri="http://localhost:8000/oauth/callback"):
    """生成授权 URL"""
    scope = "pages_messaging,pages_manage_metadata"
    base_url = "https://www.facebook.com/v18.0/dialog/oauth"

    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "token"
    }

    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook OAuth 快速设置")
    print("=" * 60)

    # 从命令行参数获取
    if len(sys.argv) > 1:
        app_id = sys.argv[1]
    else:
        app_id = input("\n请输入 Facebook App ID: ").strip()

    if not app_id:
        print("\n使用方法:")
        print("  python setup_facebook_quick.py YOUR_APP_ID")
        print("\n或运行后输入 App ID")
        sys.exit(1)

    redirect_uri = "http://localhost:8000/oauth/callback"

    # 生成授权 URL
    auth_url = generate_auth_url(app_id, redirect_uri)

    print(f"\n✓ App ID: {app_id}")
    print(f"✓ 重定向 URI: {redirect_uri}")

    print("\n" + "=" * 60)
    print("生成的授权 URL:")
    print("=" * 60)
    print(f"\n{auth_url}\n")
    print("=" * 60)

    print("\n权限范围:")
    print("- pages_messaging (必需) - 发送和接收消息")
    print("- pages_manage_metadata (可选) - 管理页面元数据")

    print("\n" + "=" * 60)
    print("下一步操作:")
    print("=" * 60)
    print("\n1. 确保在 Facebook Developer Console 中配置了重定向 URI:")
    print(f"   设置 → 基本 → 有效的 OAuth 重定向 URI")
    print(f"   添加: {redirect_uri}")
    print("\n2. 在浏览器中打开上面的授权 URL")
    print("3. 登录并授权应用")
    print("4. 从重定向 URL 中提取 access_token")
    print("5. 运行以下命令配置令牌:")
    print("   python configure_api_keys.py")
    print("\n或手动编辑 .env 文件添加:")
    print(f"   FACEBOOK_APP_ID={app_id}")
    print("   FACEBOOK_ACCESS_TOKEN=你的访问令牌")

    # 询问是否打开浏览器
    if len(sys.argv) <= 1:  # 只在交互模式下询问
        open_browser = input("\n是否在浏览器中打开授权 URL? (y/N): ").strip().lower()
        if open_browser == 'y':
            webbrowser.open(auth_url)
            print("\n✓ 已在浏览器中打开授权 URL")


if __name__ == "__main__":
    main()
