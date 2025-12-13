"""验证生产环境配置"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import yaml_config, settings
from src.config.page_token_manager import page_token_manager
from src.config.page_settings import page_settings

def verify_configurations():
    """验证所有配置"""
    print("=" * 70)
    print("生产环境配置验证")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 1. Telegram群组配置
    print("1. Telegram群组配置检查:")
    telegram_config = yaml_config.get("telegram_groups", {})
    main_group = telegram_config.get("main_group", "@your_group")
    if main_group and main_group != "@your_group":
        print(f"   ✅ Telegram群组: {main_group}")
    else:
        print(f"   ❌ Telegram群组未配置或使用默认值: {main_group}")
        all_ok = False
    print()
    
    # 2. Facebook Token配置
    print("2. Facebook Token配置检查:")
    pages = page_token_manager.list_pages()
    print(f"   📊 已配置的页面数: {len(pages)}")
    for page_id, info in pages.items():
        token = page_token_manager.get_token(page_id)
        if token:
            print(f"   ✅ 页面 {page_id}: Token已配置 ({len(token)} 字符)")
        else:
            print(f"   ❌ 页面 {page_id}: Token未配置")
            all_ok = False
    print()
    
    # 3. 页面自动回复设置
    print("3. 页面自动回复设置检查:")
    enabled_pages = []
    for page_id in page_token_manager._tokens.keys():
        if page_id == "default":
            continue
        if page_settings.is_auto_reply_enabled(page_id):
            enabled_pages.append(page_id)
            print(f"   ✅ 页面 {page_id}: 自动回复已启用")
        else:
            print(f"   ⚠️  页面 {page_id}: 自动回复已禁用")
    print(f"   📊 启用自动回复的页面数: {len(enabled_pages)}")
    print()
    
    # 4. OpenAI配置
    print("4. OpenAI配置检查:")
    if settings.openai_api_key:
        print(f"   ✅ OpenAI API Key: 已配置 ({len(settings.openai_api_key)} 字符)")
        print(f"   ✅ OpenAI Model: {settings.openai_model}")
    else:
        print("   ❌ OpenAI API Key: 未配置")
        all_ok = False
    print()
    
    # 5. 数据库配置
    print("5. 数据库配置检查:")
    if settings.database_url:
        print(f"   ✅ Database URL: 已配置")
        # 尝试连接数据库
        try:
            from src.database.database import engine
            with engine.connect() as conn:
                print("   ✅ 数据库连接: 成功")
        except Exception as e:
            print(f"   ❌ 数据库连接: 失败 - {str(e)}")
            all_ok = False
    else:
        print("   ❌ Database URL: 未配置")
        all_ok = False
    print()
    
    # 6. Telegram通知配置
    print("6. Telegram通知配置检查:")
    if settings.telegram_bot_token:
        print(f"   ✅ Telegram Bot Token: 已配置 ({len(settings.telegram_bot_token)} 字符)")
    else:
        print("   ❌ Telegram Bot Token: 未配置")
        all_ok = False
    
    if settings.telegram_chat_id:
        print(f"   ✅ Telegram Chat ID: 已配置")
    else:
        print("   ❌ Telegram Chat ID: 未配置")
        all_ok = False
    print()
    
    # 7. AI提示词配置
    print("7. AI提示词配置检查:")
    ai_templates = yaml_config.get("ai_templates", {})
    prompt_type = ai_templates.get("prompt_type")
    if prompt_type:
        print(f"   ✅ 提示词类型: {prompt_type}")
    else:
        print("   ⚠️  提示词类型: 未配置（将使用默认提示词）")
    print()
    
    # 总结
    print("=" * 70)
    if all_ok:
        print("✅ 所有关键配置检查通过！")
    else:
        print("❌ 部分配置存在问题，请修复后再部署")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    try:
        success = verify_configurations()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 配置验证过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

