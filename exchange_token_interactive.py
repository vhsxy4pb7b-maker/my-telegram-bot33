"""交互式 Facebook 长期令牌交换工具"""
import requests
import os
import sys


def read_env_value(key):
    """从 .env 文件读取值"""
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    value = line.split("=", 1)[1].strip()
                    if value and not value.startswith("your_"):
                        return value
    return None


def update_env_value(key, value):
    """更新 .env 文件中的值"""
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
        return True

    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{key}={value}\n")

    with open(".env", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return True


def main():
    print("=" * 60)
    print("Facebook 长期访问令牌交换工具")
    print("=" * 60)

    # 读取短期令牌
    print("\n步骤 1: 读取短期访问令牌...")
    short_token = read_env_value("FACEBOOK_ACCESS_TOKEN")
    if short_token:
        print(f"✓ 已从 .env 读取短期令牌: {short_token[:20]}...{short_token[-10:]}")
    else:
        print("✗ 未找到短期访问令牌")
        short_token = input("\n请输入短期访问令牌: ").strip()
        if not short_token:
            print("✗ 短期令牌不能为空")
            return

    # 读取 App ID
    print("\n步骤 2: 读取 App ID...")
    app_id = read_env_value("FACEBOOK_APP_ID")
    if app_id:
        print(f"✓ 已从 .env 读取 App ID: {app_id}")
    else:
        print("✗ 未找到 App ID")
        app_id = input("\n请输入 Facebook App ID: ").strip()
        if not app_id:
            print("✗ App ID 不能为空")
            return

    # 读取或输入 App Secret
    print("\n步骤 3: 获取 App Secret...")
    app_secret = read_env_value("FACEBOOK_APP_SECRET")
    if app_secret:
        print(f"✓ 已从 .env 读取 App Secret: {app_secret[:10]}...")
        use_existing = input("\n是否使用已保存的 App Secret? (Y/n): ").strip().lower()
        if use_existing != 'n':
            pass  # 使用已保存的
        else:
            app_secret = None

    if not app_secret:
        print("\n" + "=" * 60)
        print("获取 App Secret")
        print("=" * 60)
        print(
            "\n1. 访问: https://developers.facebook.com/apps/848496661333193/settings/basic/")
        print("2. 在'应用密钥'旁边点击'显示'")
        print("3. 输入密码确认")
        print("4. 复制 App Secret")
        print("\n" + "=" * 60)
        app_secret = input("\n请输入 Facebook App Secret: ").strip()
        if not app_secret:
            print("✗ App Secret 不能为空")
            return

        # 询问是否保存
        save_secret = input(
            "\n是否保存 App Secret 到 .env? (y/N): ").strip().lower()
        if save_secret == 'y':
            update_env_value("FACEBOOK_APP_SECRET", app_secret)
            print("✓ App Secret 已保存到 .env")

    # 交换令牌
    print("\n" + "=" * 60)
    print("步骤 4: 交换长期令牌...")
    print("=" * 60)

    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }

    print("\n正在交换令牌...")
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            long_token = data["access_token"]
            expires_in = data.get("expires_in", "N/A")
            days = int(expires_in) // 86400 if isinstance(expires_in,
                                                          (int, str)) and str(expires_in).isdigit() else "N/A"

            print("\n" + "=" * 60)
            print("✓ 令牌交换成功！")
            print("=" * 60)
            print(f"\n长期访问令牌: {long_token}")
            print(f"过期时间: {expires_in} 秒 ({days} 天)")

            # 自动更新到 .env
            print("\n正在更新 .env 文件...")
            if update_env_value("FACEBOOK_ACCESS_TOKEN", long_token):
                print("✓ 长期令牌已保存到 .env 文件")

            print("\n" + "=" * 60)
            print("✅ 完成！")
            print("=" * 60)
            print("\n长期访问令牌已配置，有效期约 60 天")
            print("运行以下命令验证:")
            print("  python check_oauth_status.py")

        else:
            print(f"\n✗ 交换失败: {data}")
            if "error" in data:
                error = data["error"]
                print(f"错误类型: {error.get('type', 'N/A')}")
                print(f"错误消息: {error.get('message', 'N/A')}")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"响应状态: {e.response.status_code}")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
