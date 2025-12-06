"""验证 Facebook OAuth 重定向 URI 配置"""
import requests
import sys


def verify_redirect_uri(app_id, redirect_uri):
    """验证重定向 URI 是否已配置"""
    print("=" * 60)
    print("验证 Facebook OAuth 重定向 URI 配置")
    print("=" * 60)

    print(f"\n应用 ID: {app_id}")
    print(f"重定向 URI: {redirect_uri}")

    # 生成测试授权 URL
    from urllib.parse import urlencode
    test_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode({
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': 'pages_messaging',
        'response_type': 'token'
    })}"

    print("\n" + "=" * 60)
    print("验证方法")
    print("=" * 60)

    print("\n1. 检查配置步骤：")
    print("   ✓ 已在 Facebook Developer Console 中添加重定向 URI")
    print("   ✓ URI 格式正确：http://localhost:8000/oauth/callback")
    print("   ✓ 已保存更改")

    print("\n2. 测试授权 URL：")
    print(f"   {test_url}")

    print("\n3. 验证步骤：")
    print("   a) 在浏览器中打开上面的测试 URL")
    print("   b) 如果看到授权页面 → 配置正确 ✓")
    print("   c) 如果看到 'redirect_uri_mismatch' 错误 → 配置有问题 ✗")

    print("\n" + "=" * 60)
    print("常见问题排查")
    print("=" * 60)

    print("\n如果看到 'redirect_uri_mismatch' 错误：")
    print("1. 检查 Facebook Developer Console 中的 URI 配置")
    print("2. 确认 URI 完全匹配（包括协议、域名、端口、路径）")
    print("3. 确认已保存更改并等待几分钟生效")
    print("4. 检查是否有多个应用使用相同的 App ID")

    print("\n" + "=" * 60)
    print("快速链接")
    print("=" * 60)
    print(
        f"\n应用设置: https://developers.facebook.com/apps/{app_id}/settings/basic/")
    print(f"应用仪表板: https://developers.facebook.com/apps/{app_id}/dashboard/")

    return test_url


if __name__ == "__main__":
    app_id = "848496661333193"
    redirect_uri = "http://localhost:8000/oauth/callback"

    if len(sys.argv) > 1:
        app_id = sys.argv[1]
    if len(sys.argv) > 2:
        redirect_uri = sys.argv[2]

    test_url = verify_redirect_uri(app_id, redirect_uri)

    print("\n" + "=" * 60)
    print("下一步")
    print("=" * 60)
    print("\n配置完成后，可以使用上面的测试 URL 验证配置")
    print("或使用之前生成的完整授权 URL 获取访问令牌")
