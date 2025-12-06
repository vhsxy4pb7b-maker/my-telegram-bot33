"""验证平台配置和注册状态"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_platform_registration():
    """检查平台注册状态"""
    print("=" * 60)
    print("检查平台注册状态")
    print("=" * 60)
    
    try:
        # 导入注册模块以确保平台被注册
        import src.facebook.register  # noqa: F401
        import src.instagram.register  # noqa: F401
        
        from src.platforms.registry import registry
        
        registered_platforms = registry.list_platforms()
        print(f"\n已注册的平台: {registered_platforms}")
        
        if "facebook" in registered_platforms:
            print("✅ Facebook平台已注册")
        else:
            print("❌ Facebook平台未注册")
        
        if "instagram" in registered_platforms:
            print("✅ Instagram平台已注册")
        else:
            print("❌ Instagram平台未注册")
        
        return True
    except Exception as e:
        print(f"❌ 检查平台注册时出错: {str(e)}")
        return False


def check_database_models():
    """检查数据库模型"""
    print("\n" + "=" * 60)
    print("检查数据库模型")
    print("=" * 60)
    
    try:
        from src.database.models import Platform, Customer, Conversation
        
        # 检查Platform枚举
        platforms = [p.value for p in Platform]
        print(f"\n支持的平台枚举: {platforms}")
        
        # 检查Customer模型字段
        customer_fields = [col.name for col in Customer.__table__.columns]
        required_fields = ['platform', 'platform_user_id', 'facebook_id']
        print(f"\nCustomer表字段: {customer_fields}")
        
        for field in required_fields:
            if field in customer_fields:
                print(f"✅ Customer.{field} 字段存在")
            else:
                print(f"❌ Customer.{field} 字段缺失")
        
        # 检查Conversation模型字段
        conversation_fields = [col.name for col in Conversation.__table__.columns]
        required_fields = ['platform', 'platform_message_id', 'facebook_message_id']
        print(f"\nConversation表字段: {conversation_fields}")
        
        for field in required_fields:
            if field in conversation_fields:
                print(f"✅ Conversation.{field} 字段存在")
            else:
                print(f"❌ Conversation.{field} 字段缺失")
        
        return True
    except Exception as e:
        print(f"❌ 检查数据库模型时出错: {str(e)}")
        return False


def check_config():
    """检查配置"""
    print("\n" + "=" * 60)
    print("检查配置")
    print("=" * 60)
    
    try:
        from src.config import settings
        
        # 检查Facebook配置
        print("\nFacebook配置:")
        print(f"  APP_ID: {'✅ 已配置' if hasattr(settings, 'facebook_app_id') and settings.facebook_app_id else '❌ 未配置'}")
        print(f"  ACCESS_TOKEN: {'✅ 已配置' if hasattr(settings, 'facebook_access_token') and settings.facebook_access_token else '❌ 未配置'}")
        print(f"  VERIFY_TOKEN: {'✅ 已配置' if hasattr(settings, 'facebook_verify_token') and settings.facebook_verify_token else '❌ 未配置'}")
        
        # 检查Instagram配置
        print("\nInstagram配置:")
        instagram_token = getattr(settings, 'instagram_access_token', None) or getattr(settings, 'facebook_access_token', None)
        instagram_verify = getattr(settings, 'instagram_verify_token', None) or getattr(settings, 'facebook_verify_token', None)
        instagram_user_id = getattr(settings, 'instagram_user_id', None)
        
        print(f"  ACCESS_TOKEN: {'✅ 已配置' if instagram_token else '⚠️  使用Facebook配置'}")
        print(f"  VERIFY_TOKEN: {'✅ 已配置' if instagram_verify else '⚠️  使用Facebook配置'}")
        print(f"  USER_ID: {'✅ 已配置' if instagram_user_id else '❌ 未配置（发送消息需要）'}")
        
        return True
    except Exception as e:
        print(f"❌ 检查配置时出错: {str(e)}")
        return False


def check_imports():
    """检查关键模块导入"""
    print("\n" + "=" * 60)
    print("检查模块导入")
    print("=" * 60)
    
    modules = [
        ("src.platforms.base", "PlatformClient"),
        ("src.platforms.registry", "registry"),
        ("src.platforms.manager", "platform_manager"),
        ("src.facebook.api_client", "FacebookAPIClient"),
        ("src.facebook.message_parser", "FacebookMessageParser"),
        ("src.instagram.api_client", "InstagramAPIClient"),
        ("src.instagram.message_parser", "InstagramMessageParser"),
        ("src.main_processor", "process_platform_message"),
    ]
    
    all_ok = True
    for module_path, item_name in modules:
        try:
            module = __import__(module_path, fromlist=[item_name])
            getattr(module, item_name)
            print(f"✅ {module_path}.{item_name}")
        except Exception as e:
            print(f"❌ {module_path}.{item_name} - {str(e)}")
            all_ok = False
    
    return all_ok


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("多平台客服系统 - 配置验证")
    print("=" * 60)
    
    results = []
    
    results.append(("模块导入", check_imports()))
    results.append(("平台注册", check_platform_registration()))
    results.append(("数据库模型", check_database_models()))
    results.append(("配置检查", check_config()))
    
    print("\n" + "=" * 60)
    print("验证结果总结")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有检查通过！系统已准备就绪。")
    else:
        print("⚠️  部分检查未通过，请查看上述错误信息。")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

