"""检查 Facebook 应用配置的辅助工具"""
import webbrowser


def main():
    """显示配置检查清单"""
    print("=" * 60)
    print("Facebook 应用配置检查清单")
    print("=" * 60)

    app_id = "848496661333193"
    settings_url = f"https://developers.facebook.com/apps/{app_id}/settings/basic/"

    print(f"\n应用 ID: {app_id}")
    print(f"\n应用设置页面: {settings_url}")

    print("\n" + "=" * 60)
    print("必须配置的项目（3项）")
    print("=" * 60)

    configs = [
        {
            "name": "应用域名（App Domains）",
            "value": "localhost",
            "location": "基本设置 → 应用域名",
            "important": "⚠️ 必需 - 解决当前错误"
        },
        {
            "name": "网站 URL（Site URL）",
            "value": "http://localhost:8000",
            "location": "基本设置 → 网站 → 添加平台",
            "important": "⚠️ 必需"
        },
        {
            "name": "OAuth 重定向 URI",
            "value": "http://localhost:8000/oauth/callback",
            "location": "基本设置 → 有效的 OAuth 重定向 URI",
            "important": "⚠️ 必需"
        }
    ]

    for i, config in enumerate(configs, 1):
        print(f"\n{i}. {config['name']}")
        print(f"   位置: {config['location']}")
        print(f"   值: {config['value']}")
        print(f"   {config['important']}")

    print("\n" + "=" * 60)
    print("配置步骤")
    print("=" * 60)

    print("\n1. 访问应用设置页面（上面的链接）")
    print("2. 依次配置上述 3 个项目")
    print("3. 保存所有更改")
    print("4. 等待 5-10 分钟让更改生效")
    print("5. 重新访问授权 URL 测试")

    print("\n" + "=" * 60)
    print("授权 URL（配置完成后使用）")
    print("=" * 60)

    auth_url = "https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token"

    print(f"\n{auth_url}")

    print("\n" + "=" * 60)
    print("操作选项")
    print("=" * 60)

    print("\n1. 打开应用设置页面")
    print("2. 打开授权 URL（配置完成后测试）")
    print("3. 查看详细配置指南")

    choice = input("\n请选择 (1/2/3) [直接回车跳过]: ").strip()

    if choice == "1":
        webbrowser.open(settings_url)
        print("\n✓ 已在浏览器中打开应用设置页面")
    elif choice == "2":
        webbrowser.open(auth_url)
        print("\n✓ 已在浏览器中打开授权 URL")
    elif choice == "3":
        print("\n详细指南: COMPLETE_FACEBOOK_SETUP.md")

    print("\n" + "=" * 60)
    print("提示")
    print("=" * 60)
    print("\n配置完成后，等待几分钟再测试")
    print("如果仍有错误，检查所有配置项是否都已保存")


if __name__ == "__main__":
    main()
