"""Facebook OAuth 授权辅助工具"""
import urllib.parse
from src.config import settings


def generate_oauth_url(app_id=None, redirect_uri=None, scope=None):
    """
    生成 Facebook OAuth 授权 URL

    Args:
        app_id: Facebook 应用 ID（如果为 None，从 .env 读取）
        redirect_uri: 重定向 URI
        scope: 权限范围（如果为 None，使用默认值）

    Returns:
        授权 URL
    """
    # 从配置读取或使用参数
    if app_id is None:
        app_id = settings.facebook_app_id
        if app_id == "your_facebook_app_id":
            app_id = input("请输入 Facebook App ID: ").strip()

    if redirect_uri is None:
        redirect_uri = input(
            "请输入重定向 URI [http://localhost:8000/oauth/callback]: ").strip()
        if not redirect_uri:
            redirect_uri = "http://localhost:8000/oauth/callback"

    if scope is None:
        scope = "pages_messaging,pages_manage_metadata"

    # 构建授权 URL
    base_url = "https://www.facebook.com/v18.0/dialog/oauth"

    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "token"
    }

    # 生成完整 URL
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{base_url}?{query_string}"

    return auth_url, params


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook OAuth 授权 URL 生成工具")
    print("=" * 60)

    print("\n本工具将帮助您生成 Facebook OAuth 授权 URL")
    print("用于获取长期访问令牌（Long-lived Access Token）")

    print("\n" + "-" * 60)
    print("步骤说明：")
    print("1. 生成授权 URL")
    print("2. 在浏览器中打开 URL")
    print("3. 授权后，从重定向 URL 中提取访问令牌")
    print("4. 将令牌保存到 .env 文件")
    print("-" * 60)

    try:
        # 生成授权 URL
        auth_url, params = generate_oauth_url()

        print("\n" + "=" * 60)
        print("生成的授权 URL")
        print("=" * 60)
        print(f"\n{auth_url}\n")

        print("=" * 60)
        print("参数说明")
        print("=" * 60)
        print(f"应用 ID (client_id): {params['client_id']}")
        print(f"重定向 URI (redirect_uri): {params['redirect_uri']}")
        print(f"权限范围 (scope): {params['scope']}")
        print(f"响应类型 (response_type): {params['response_type']}")

        print("\n" + "=" * 60)
        print("下一步操作")
        print("=" * 60)
        print("\n1. 复制上面的授权 URL")
        print("2. 在浏览器中打开该 URL")
        print("3. 登录并授权应用")
        print("4. 授权后，浏览器会重定向到 redirect_uri")
        print("5. 从重定向 URL 的 fragment 中提取 access_token")
        print("   格式: http://localhost:8000/oauth/callback#access_token=TOKEN&...")
        print("6. 复制 access_token 值")
        print("7. 运行: python configure_api_keys.py 配置令牌")

        print("\n" + "=" * 60)
        print("权限说明")
        print("=" * 60)
        print("pages_messaging - 发送和接收消息")
        print("pages_manage_metadata - 管理页面元数据")

        # 询问是否打开浏览器
        open_browser = input("\n是否在浏览器中打开授权 URL? (y/N): ").strip().lower()
        if open_browser == 'y':
            import webbrowser
            webbrowser.open(auth_url)
            print("\n✓ 已在浏览器中打开授权 URL")

    except KeyboardInterrupt:
        print("\n\n已取消操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")


if __name__ == "__main__":
    main()
