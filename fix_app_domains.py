"""修复 Facebook 应用域名配置的辅助工具"""
import webbrowser


def main():
    """显示配置说明"""
    print("=" * 60)
    print("修复 Facebook 应用域名配置")
    print("=" * 60)

    print("\n错误原因：")
    print("应用域名未配置，需要在 Facebook Developer Console 中添加")

    print("\n" + "=" * 60)
    print("需要配置的项目")
    print("=" * 60)

    print("\n1. 应用域名（App Domains）")
    print("   添加: localhost")

    print("\n2. 网站 URL（Site URL）")
    print("   添加: http://localhost:8000")

    print("\n3. OAuth 重定向 URI")
    print("   添加: http://localhost:8000/oauth/callback")

    print("\n" + "=" * 60)
    print("快速链接")
    print("=" * 60)

    settings_url = "https://developers.facebook.com/apps/848496661333193/settings/basic/"
    print(f"\n应用设置页面: {settings_url}")

    print("\n" + "=" * 60)
    print("配置步骤")
    print("=" * 60)

    print("\n1. 访问上面的应用设置页面链接")
    print("2. 找到'应用域名'（App Domains）字段")
    print("3. 添加: localhost")
    print("4. 找到'网站'部分，添加平台 → 网站")
    print("5. 输入网站 URL: http://localhost:8000")
    print("6. 确认'OAuth 重定向 URI'已配置")
    print("7. 保存所有更改")
    print("8. 等待几分钟让更改生效")

    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)

    auth_url = "https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token"

    print(f"\n配置完成后，重新访问授权 URL:")
    print(f"{auth_url}")

    open_settings = input("\n是否在浏览器中打开应用设置页面? (y/N): ").strip().lower()
    if open_settings == 'y':
        webbrowser.open(settings_url)
        print("\n✓ 已在浏览器中打开应用设置页面")

    print("\n详细说明请查看: FIX_APP_DOMAINS.md")


if __name__ == "__main__":
    main()
