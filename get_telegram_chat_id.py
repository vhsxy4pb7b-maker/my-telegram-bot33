"""获取 Telegram Chat ID 工具"""
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

def main():
    print("=" * 60)
    print("获取 Telegram Chat ID")
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
        bot_token = input("请输入 Telegram Bot Token: ").strip()
        if not bot_token:
            print("✗ Bot Token 不能为空")
            return
    
    print(f"\n✓ 使用 Bot Token: {bot_token[:10]}...")
    
    # 获取更新
    print("\n" + "=" * 60)
    print("获取 Chat ID")
    print("=" * 60)
    print("\n重要提示:")
    print("1. 请先向您的 Bot 发送一条消息（例如：/start 或 hello）")
    print("2. 发送消息后，按 Enter 继续...")
    print("\n等待您向 Bot 发送消息...")
    input("\n按 Enter 继续获取 Chat ID...")
    
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
                    for chat_id, chat_type, chat_title in sorted(chat_ids):
                        print(f"  - Chat ID: {chat_id} ({chat_type}) - {chat_title}")
                    
                    print("\n" + "=" * 60)
                    selected = input("\n请输入要使用的 Chat ID (或按 Enter 使用第一个): ").strip()
                    
                    if not selected:
                        selected = list(chat_ids)[0][0]
                    
                    if selected.isdigit() or (selected.startswith('-') and selected[1:].isdigit()):
                        print(f"\n✓ 已选择 Chat ID: {selected}")
                        print("\n请将此 Chat ID 添加到 .env 文件:")
                        print(f"TELEGRAM_CHAT_ID={selected}")
                        
                        save = input("\n是否自动保存到 .env? (y/N): ").strip().lower()
                        if save == 'y':
                            from configure_other_keys import update_env_file
                            if update_env_file("TELEGRAM_CHAT_ID", selected):
                                print("✓ Chat ID 已保存到 .env 文件")
                    else:
                        print("✗ 无效的 Chat ID")
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
        else:
            print(f"\n✗ 获取失败: {data.get('description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 请求失败: {e}")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")

if __name__ == "__main__":
    main()

