"""自动交换长期令牌（使用已配置的信息）"""
import requests
import os

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
    print("Facebook 长期访问令牌自动交换")
    print("=" * 60)
    
    # 读取配置
    print("\n读取配置...")
    short_token = read_env_value("FACEBOOK_ACCESS_TOKEN")
    app_id = read_env_value("FACEBOOK_APP_ID")
    app_secret = read_env_value("FACEBOOK_APP_SECRET")
    
    if not short_token:
        print("✗ 未找到短期访问令牌")
        return
    
    if not app_id:
        print("✗ 未找到 App ID")
        return
    
    if not app_secret:
        print("✗ 未找到 App Secret")
        return
    
    print(f"✓ 短期令牌: {short_token[:20]}...{short_token[-10:]}")
    print(f"✓ App ID: {app_id}")
    print(f"✓ App Secret: {app_secret[:10]}...")
    
    # 交换令牌
    print("\n" + "=" * 60)
    print("正在交换长期令牌...")
    print("=" * 60)
    
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" in data:
            long_token = data["access_token"]
            expires_in = data.get("expires_in", "N/A")
            days = int(expires_in) // 86400 if isinstance(expires_in, (int, str)) and str(expires_in).isdigit() else "N/A"
            
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
                print(f"错误代码: {error.get('code', 'N/A')}")
            
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
    main()

