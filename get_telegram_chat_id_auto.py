"""自动获取 Telegram Chat ID（无需等待输入）"""
import requests
import sys
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

def update_env_file(key, value):
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
        if line.strip().startswith(f"{key}="):
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
    print("自动获取 Telegram Chat ID")
    print("=" * 60)
    
    # 从命令行参数读取 Bot Token
    bot_token = None
    if len(sys.argv) > 1:
        bot_token = sys.argv[1].strip()
        print(f"\n✓ 从命令行参数读取 Bot Token: {bot_token[:10]}...")
    
    # 从 .env 文件读取
    if not bot_token:
        bot_token = read_env_value("TELEGRAM_BOT_TOKEN")
        if bot_token:
            print(f"\n✓ 从 .env 读取 Bot Token: {bot_token[:10]}...")
    
    # 提示输入
    if not bot_token:
        print("\n未找到 Telegram Bot Token")
        print("使用方法: python get_telegram_chat_id_auto.py YOUR_BOT_TOKEN")
        return
    
    print(f"\n✓ 使用 Bot Token: {bot_token[:10]}...")
    
    # 直接获取更新
    print("\n" + "=" * 60)
    print("正在获取 Chat ID...")
    print("=" * 60)
    print("\n提示: 如果未找到消息，请先向 Bot 发送一条消息")
    print("然后重新运行此工具")
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            updates = data.get("result", [])
            if updates:
                print("\n" + "=" * 60)
                print("找到的 Chat ID:")
                print("=" * 60)
                
                chat_ids = set()
                for update in updates:
                    message = update.get("message", {})
                    chat = message.get("chat", {})
                    chat_id = chat.get("id")
                    chat_type = chat.get("type", "unknown")
                    chat_title = chat.get("title") or chat.get("first_name") or chat.get("username") or "Unknown"
                    
                    if chat_id:
                        chat_ids.add((chat_id, chat_type, chat_title))
                
                if chat_ids:
                    print("\n可用的 Chat ID:")
                    for idx, (chat_id, chat_type, chat_title) in enumerate(sorted(chat_ids), 1):
                        print(f"  {idx}. Chat ID: {chat_id} ({chat_type}) - {chat_title}")
                    
                    # 自动选择第一个
                    selected = list(chat_ids)[0][0]
                    print("\n" + "=" * 60)
                    print(f"✓ 自动选择第一个 Chat ID: {selected}")
                    
                    # 自动保存
                    print("\n正在保存到 .env 文件...")
                    if update_env_file("TELEGRAM_CHAT_ID", str(selected)):
                        print("✓ Chat ID 已保存到 .env 文件")
                    
                    # 同时保存 Bot Token（如果还没有）
                    existing_token = read_env_value("TELEGRAM_BOT_TOKEN")
                    if not existing_token:
                        if update_env_file("TELEGRAM_BOT_TOKEN", bot_token):
                            print("✓ Bot Token 已保存到 .env 文件")
                    
                    print("\n" + "=" * 60)
                    print("✅ 完成！")
                    print("=" * 60)
                    print(f"\n已配置:")
                    print(f"  - TELEGRAM_BOT_TOKEN: {bot_token[:10]}...")
                    print(f"  - TELEGRAM_CHAT_ID: {selected}")
                    print("\n运行以下命令验证配置:")
                    print("  python verify_setup.py")
                else:
                    print("\n⚠ 未找到任何消息")
                    print("请确保：")
                    print("1. Bot Token 正确")
                    print("2. 已向 Bot 发送消息")
                    print("3. Bot 已添加到群组或私聊")
            else:
                print("\n⚠ 未找到任何更新")
                print("请确保：")
                print("1. Bot Token 正确")
                print("2. 已向 Bot 发送消息")
                print("3. 发送消息后等待几秒钟再运行此工具")
        else:
            error_msg = data.get('description', 'Unknown error')
            print(f"\n✗ 获取失败: {error_msg}")
            if "Unauthorized" in error_msg:
                print("提示: Bot Token 可能不正确，请检查")
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 请求失败: {e}")
        print("请检查网络连接")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")

if __name__ == "__main__":
    main()

