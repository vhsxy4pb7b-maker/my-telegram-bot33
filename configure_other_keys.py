"""配置其他 API 密钥（OpenAI 和 Telegram）"""
import os
import sys


def update_env_file(key, value):
    """更新 .env 文件中的值"""
    env_file = ".env"

    if not os.path.exists(env_file):
        print(f"✗ .env 文件不存在")
        return False

    # 读取文件
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 更新或添加配置
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        # 如果不存在，添加到文件末尾
        new_lines.append(f"{key}={value}\n")

    # 写回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    return True


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


def configure_openai():
    """配置 OpenAI API"""
    print("\n" + "=" * 60)
    print("配置 OpenAI API")
    print("=" * 60)
    
    # 检查是否已配置
    existing_key = read_env_value("OPENAI_API_KEY")
    if existing_key:
        print(f"\n✓ 已存在 OpenAI API Key: {existing_key[:10]}...{existing_key[-5:]}")
        update = input("是否更新? (y/N): ").strip().lower()
        if update != 'y':
            print("已跳过 OpenAI API 配置")
            return True
    
    print("\n需要从 OpenAI Platform 获取：")
    print("网址: https://platform.openai.com/api-keys")
    print("\n步骤：")
    print("1. 登录或注册 OpenAI 账号")
    print("2. 访问 https://platform.openai.com/api-keys")
    print("3. 点击 'Create new secret key'")
    print("4. 复制生成的密钥（只显示一次，请妥善保存）")
    print("\n详细步骤请参考: API_KEYS_GUIDE.md")

    api_key = input("\nOPENAI_API_KEY [留空跳过]: ").strip()
    if api_key:
        update_env_file("OPENAI_API_KEY", api_key)
        print("✓ OPENAI_API_KEY 已保存")
        return True
    else:
        print("⚠️  已跳过 OpenAI API 配置")
        return False


def configure_telegram():
    """配置 Telegram Bot"""
    print("\n" + "=" * 60)
    print("配置 Telegram Bot")
    print("=" * 60)
    
    # 检查是否已配置
    existing_token = read_env_value("TELEGRAM_BOT_TOKEN")
    existing_chat_id = read_env_value("TELEGRAM_CHAT_ID")
    
    if existing_token:
        print(f"\n✓ 已存在 Telegram Bot Token: {existing_token[:10]}...")
        update_token = input("是否更新 Bot Token? (y/N): ").strip().lower()
    else:
        update_token = 'y'
    
    if existing_chat_id:
        print(f"✓ 已存在 Telegram Chat ID: {existing_chat_id}")
        update_chat = input("是否更新 Chat ID? (y/N): ").strip().lower()
    else:
        update_chat = 'y'
    
    if update_token != 'y' and update_chat != 'y':
        print("已跳过 Telegram Bot 配置")
        return bool(existing_token and existing_chat_id)
    
    print("\n需要创建 Telegram Bot：")
    print("1. 在 Telegram 中搜索 @BotFather")
    print("2. 发送 /newbot 命令创建 Bot")
    print("3. 按照提示设置 Bot 名称和用户名")
    print("4. 复制返回的 Bot Token")
    print("\n获取 Chat ID：")
    print("方法 1: 通过 Bot 获取")
    print("  1. 将 Bot 添加到群组或私聊")
    print("  2. 发送消息给 Bot")
    print("  3. 访问: https://api.telegram.org/bot<TOKEN>/getUpdates")
    print("  4. 在返回的 JSON 中找到 chat.id")
    print("\n方法 2: 使用工具获取")
    print("  运行: python get_telegram_chat_id.py")
    print("\n详细步骤请参考: API_KEYS_GUIDE.md")

    if update_token == 'y':
        bot_token = input("\nTELEGRAM_BOT_TOKEN [留空跳过]: ").strip()
        if bot_token:
            update_env_file("TELEGRAM_BOT_TOKEN", bot_token)
            print("✓ TELEGRAM_BOT_TOKEN 已保存")
        else:
            bot_token = existing_token
    else:
        bot_token = existing_token

    if update_chat == 'y':
        chat_id = input("TELEGRAM_CHAT_ID [留空跳过]: ").strip()
        if chat_id:
            update_env_file("TELEGRAM_CHAT_ID", chat_id)
            print("✓ TELEGRAM_CHAT_ID 已保存")
        else:
            chat_id = existing_chat_id
    else:
        chat_id = existing_chat_id

    return bool(bot_token and chat_id)


def main():
    """主函数"""
    print("=" * 60)
    print("配置其他 API 密钥")
    print("=" * 60)
    print("\n本工具将帮助您配置 OpenAI 和 Telegram API 密钥")
    print("Facebook API 已配置，将跳过")
    print("\n您可以随时按 Ctrl+C 退出，稍后继续")
    print("提示：如果还没有获取 API 密钥，请先参考 API_KEYS_GUIDE.md")

    configured = []

    try:
        # OpenAI API
        if configure_openai():
            configured.append("OpenAI API")

        # Telegram Bot
        if configure_telegram():
            configured.append("Telegram Bot")

        # 总结
        print("\n" + "=" * 60)
        print("配置完成总结")
        print("=" * 60)

        if configured:
            print(f"\n✓ 已完成的配置: {', '.join(configured)}")
        else:
            print("\n⚠️  没有完成任何配置")
            print("您可以稍后手动编辑 .env 文件或重新运行此脚本")

        print("\n下一步：")
        print("1. 验证配置: python verify_setup.py")
        print("2. 启动服务: python run.py")
        print("3. 访问 API 文档: http://localhost:8000/docs")

    except KeyboardInterrupt:
        print("\n\n配置已中断，已完成的配置已保存")
        print("可以稍后继续运行此脚本完成剩余配置")


if __name__ == "__main__":
    main()

