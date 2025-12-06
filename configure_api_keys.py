"""API 密钥配置工具"""
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


def configure_facebook():
    """配置 Facebook API"""
    print("\n" + "=" * 60)
    print("配置 Facebook API")
    print("=" * 60)
    print("\n需要从 Facebook Developer Console 获取：")
    print("网址: https://developers.facebook.com/")
    print("\n详细步骤请参考: API_KEYS_GUIDE.md")

    print("\n请输入 Facebook API 配置：")
    app_id = input("FACEBOOK_APP_ID [留空跳过]: ").strip()
    if app_id:
        update_env_file("FACEBOOK_APP_ID", app_id)
        print("✓ FACEBOOK_APP_ID 已保存")

    app_secret = input("FACEBOOK_APP_SECRET [留空跳过]: ").strip()
    if app_secret:
        update_env_file("FACEBOOK_APP_SECRET", app_secret)
        print("✓ FACEBOOK_APP_SECRET 已保存")

    access_token = input("FACEBOOK_ACCESS_TOKEN [留空跳过]: ").strip()
    if access_token:
        update_env_file("FACEBOOK_ACCESS_TOKEN", access_token)
        print("✓ FACEBOOK_ACCESS_TOKEN 已保存")

    verify_token = input("FACEBOOK_VERIFY_TOKEN [留空使用默认]: ").strip()
    if not verify_token:
        import secrets
        verify_token = secrets.token_urlsafe(16)
        print(f"使用自动生成的验证令牌: {verify_token}")
    update_env_file("FACEBOOK_VERIFY_TOKEN", verify_token)
    print("✓ FACEBOOK_VERIFY_TOKEN 已保存")

    return bool(app_id and app_secret and access_token)


def configure_openai():
    """配置 OpenAI API"""
    print("\n" + "=" * 60)
    print("配置 OpenAI API")
    print("=" * 60)
    print("\n需要从 OpenAI Platform 获取：")
    print("网址: https://platform.openai.com/api-keys")
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
    print("\n需要创建 Telegram Bot：")
    print("1. 在 Telegram 中搜索 @BotFather")
    print("2. 发送 /newbot 命令创建 Bot")
    print("3. 复制返回的 Bot Token")
    print("\n获取 Chat ID：")
    print("1. 将 Bot 添加到群组或私聊")
    print("2. 发送消息给 Bot")
    print("3. 访问: https://api.telegram.org/bot<TOKEN>/getUpdates")
    print("4. 在返回的 JSON 中找到 chat.id")
    print("\n详细步骤请参考: API_KEYS_GUIDE.md")

    bot_token = input("\nTELEGRAM_BOT_TOKEN [留空跳过]: ").strip()
    if bot_token:
        update_env_file("TELEGRAM_BOT_TOKEN", bot_token)
        print("✓ TELEGRAM_BOT_TOKEN 已保存")

    chat_id = input("TELEGRAM_CHAT_ID [留空跳过]: ").strip()
    if chat_id:
        update_env_file("TELEGRAM_CHAT_ID", chat_id)
        print("✓ TELEGRAM_CHAT_ID 已保存")

    return bool(bot_token and chat_id)


def main():
    """主函数"""
    print("=" * 60)
    print("API 密钥配置工具")
    print("=" * 60)
    print("\n本工具将帮助您配置系统所需的 API 密钥")
    print("您可以随时按 Ctrl+C 退出，稍后继续")
    print("\n提示：如果还没有获取 API 密钥，请先参考 API_KEYS_GUIDE.md")

    configured = []

    try:
        # Facebook API
        if configure_facebook():
            configured.append("Facebook API")

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
