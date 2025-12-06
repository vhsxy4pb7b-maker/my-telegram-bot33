"""Facebook OAuth 完整设置向导"""
import urllib.parse
import webbrowser
import sys


def step1_check_app_id():
    """步骤 1: 检查或输入 App ID"""
    print("=" * 60)
    print("步骤 1: Facebook App ID")
    print("=" * 60)

    print("\n如果您还没有 App ID，请：")
    print("1. 访问: https://developers.facebook.com/")
    print("2. 创建应用（选择'业务'类型）")
    print("3. 在'设置' → '基本'中获取 App ID")

    app_id = input("\n请输入 Facebook App ID [留空跳过]: ").strip()

    if app_id:
        print(f"✓ App ID: {app_id}")
        return app_id
    else:
        print("⚠️  已跳过，稍后可以手动配置")
        return None


def step2_configure_redirect_uri():
    """步骤 2: 配置重定向 URI"""
    print("\n" + "=" * 60)
    print("步骤 2: 配置重定向 URI")
    print("=" * 60)

    redirect_uri = "http://localhost:8000/oauth/callback"

    print(f"\n默认重定向 URI: {redirect_uri}")
    print("\n需要在 Facebook Developer Console 中配置：")
    print("1. 访问: https://developers.facebook.com/")
    print("2. 选择您的应用")
    print("3. 进入'设置' → '基本'")
    print("4. 在'有效的 OAuth 重定向 URI'中添加：")
    print(f"   {redirect_uri}")

    use_default = input(
        f"\n使用默认 URI ({redirect_uri})? (Y/n): ").strip().lower()

    if use_default == 'n':
        redirect_uri = input("请输入自定义重定向 URI: ").strip()

    print(f"✓ 重定向 URI: {redirect_uri}")
    return redirect_uri


def step3_generate_auth_url(app_id, redirect_uri):
    """步骤 3: 生成授权 URL"""
    print("\n" + "=" * 60)
    print("步骤 3: 生成授权 URL")
    print("=" * 60)

    if not app_id:
        print("✗ 需要 App ID 才能生成授权 URL")
        return None

    scope = "pages_messaging,pages_manage_metadata"

    base_url = "https://www.facebook.com/v18.0/dialog/oauth"
    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "token"
    }

    query_string = urllib.parse.urlencode(params)
    auth_url = f"{base_url}?{query_string}"

    print("\n生成的授权 URL:")
    print("-" * 60)
    print(auth_url)
    print("-" * 60)

    print("\n权限范围:")
    print("- pages_messaging (必需) - 发送和接收消息")
    print("- pages_manage_metadata (可选) - 管理页面元数据")

    return auth_url


def step4_get_access_token():
    """步骤 4: 获取访问令牌"""
    print("\n" + "=" * 60)
    print("步骤 4: 获取访问令牌")
    print("=" * 60)

    print("\n操作步骤：")
    print("1. 在浏览器中打开上面的授权 URL")
    print("2. 登录您的 Facebook 账号")
    print("3. 授权应用权限")
    print("4. 授权后，浏览器会重定向")
    print("5. 从重定向 URL 中提取 access_token")
    print("\n重定向 URL 格式：")
    print("http://localhost:8000/oauth/callback#access_token=TOKEN&token_type=bearer&expires_in=5183944")
    print("\n复制 access_token 的值（TOKEN 部分）")

    access_token = input("\n请输入获取的 access_token [留空跳过]: ").strip()

    if access_token:
        print(f"✓ 访问令牌已获取（长度: {len(access_token)} 字符）")
        return access_token
    else:
        print("⚠️  已跳过，稍后可以手动配置")
        return None


def step5_exchange_long_token(short_token, app_id, app_secret):
    """步骤 5: 交换长期令牌"""
    print("\n" + "=" * 60)
    print("步骤 5: 交换长期访问令牌（可选）")
    print("=" * 60)

    if not short_token:
        print("⚠️  需要访问令牌才能交换")
        return None

    print("\n短期令牌有效期：1-2 小时")
    print("长期令牌有效期：60 天")

    exchange = input("\n是否交换为长期令牌? (y/N): ").strip().lower()

    if exchange != 'y':
        print("已跳过，使用短期令牌")
        return short_token

    if not app_id or not app_secret:
        app_id = input("请输入 App ID: ").strip()
        app_secret = input("请输入 App Secret: ").strip()

    if not app_id or not app_secret:
        print("✗ 需要 App ID 和 App Secret")
        return short_token

    try:
        import requests
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": short_token
        }

        print("\n正在交换令牌...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            long_token = data["access_token"]
            expires_in = data.get("expires_in", "N/A")
            days = int(
                expires_in) // 86400 if isinstance(expires_in, int) else "N/A"

            print(f"\n✓ 长期令牌获取成功！")
            print(f"有效期: {expires_in} 秒 ({days} 天)")
            return long_token
        else:
            print(f"✗ 交换失败: {data}")
            return short_token

    except ImportError:
        print("✗ requests 库未安装，无法交换令牌")
        return short_token
    except Exception as e:
        print(f"✗ 交换失败: {e}")
        return short_token


def step6_save_to_env(app_id, app_secret, access_token, verify_token):
    """步骤 6: 保存到 .env 文件"""
    print("\n" + "=" * 60)
    print("步骤 6: 保存配置到 .env 文件")
    print("=" * 60)

    import os

    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"✗ .env 文件不存在")
        return False

    # 读取文件
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 更新配置
    updated = {}
    new_lines = []

    for line in lines:
        updated_line = line
        if app_id and line.startswith("FACEBOOK_APP_ID="):
            updated_line = f"FACEBOOK_APP_ID={app_id}\n"
            updated["FACEBOOK_APP_ID"] = True
        elif app_secret and line.startswith("FACEBOOK_APP_SECRET="):
            updated_line = f"FACEBOOK_APP_SECRET={app_secret}\n"
            updated["FACEBOOK_APP_SECRET"] = True
        elif access_token and line.startswith("FACEBOOK_ACCESS_TOKEN="):
            updated_line = f"FACEBOOK_ACCESS_TOKEN={access_token}\n"
            updated["FACEBOOK_ACCESS_TOKEN"] = True
        elif verify_token and line.startswith("FACEBOOK_VERIFY_TOKEN="):
            updated_line = f"FACEBOOK_VERIFY_TOKEN={verify_token}\n"
            updated["FACEBOOK_VERIFY_TOKEN"] = True

        new_lines.append(updated_line)

    # 写回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    if updated:
        print("\n✓ 已更新以下配置：")
        for key in updated:
            print(f"  - {key}")
    else:
        print("\n⚠️  没有更新任何配置")

    return True


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook OAuth 完整设置向导")
    print("=" * 60)
    print("\n本向导将帮助您完成 Facebook OAuth 的完整配置")
    print("包括：App ID、授权 URL、访问令牌、长期令牌等")

    try:
        # 步骤 1: App ID
        app_id = step1_check_app_id()

        # 步骤 2: 重定向 URI
        redirect_uri = step2_configure_redirect_uri()

        # 步骤 3: 生成授权 URL
        auth_url = step3_generate_auth_url(
            app_id, redirect_uri) if app_id else None

        # 询问是否打开浏览器
        if auth_url:
            open_browser = input("\n是否在浏览器中打开授权 URL? (y/N): ").strip().lower()
            if open_browser == 'y':
                webbrowser.open(auth_url)
                print("✓ 已在浏览器中打开")

        # 步骤 4: 获取访问令牌
        access_token = step4_get_access_token()

        # 步骤 5: 交换长期令牌
        if access_token:
            app_secret = input("\n请输入 App Secret（用于交换长期令牌）[留空跳过]: ").strip()
            long_token = step5_exchange_long_token(
                access_token, app_id, app_secret) if app_secret else access_token
            if long_token != access_token:
                access_token = long_token
                print("✓ 已使用长期令牌")

        # 步骤 6: 保存配置
        import secrets
        verify_token = secrets.token_urlsafe(16)

        app_secret = input("\n请输入 App Secret（保存到配置）[留空跳过]: ").strip(
        ) if not 'app_secret' in locals() else app_secret

        if app_id or app_secret or access_token:
            step6_save_to_env(app_id, app_secret, access_token, verify_token)

        # 总结
        print("\n" + "=" * 60)
        print("配置完成总结")
        print("=" * 60)

        configured = []
        if app_id:
            configured.append("App ID")
        if app_secret:
            configured.append("App Secret")
        if access_token:
            configured.append("Access Token")
        if verify_token:
            configured.append("Verify Token")

        if configured:
            print(f"\n✓ 已配置: {', '.join(configured)}")
        else:
            print("\n⚠️  没有完成配置")

        print("\n下一步：")
        print("1. 验证配置: python verify_setup.py")
        print("2. 配置 Webhook: 在 Facebook Developer Console 中设置")
        print("3. 测试连接: 发送测试消息")

    except KeyboardInterrupt:
        print("\n\n配置已中断，已完成的配置已保存")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
