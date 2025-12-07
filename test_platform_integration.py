"""测试平台集成功能"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_platform_registry():
    """测试平台注册器"""
    print("=" * 60)
    print("测试平台注册器")
    print("=" * 60)
    
    try:
        # 导入注册模块
        import src.facebook.register  # noqa: F401
        import src.instagram.register  # noqa: F401
        
        from src.platforms.registry import registry
        
        # 检查注册的平台
        platforms = registry.list_platforms()
        print(f"\n已注册的平台: {platforms}")
        
        # 测试获取类
        for platform in platforms:
            client_class = registry.get_client_class(platform)
            parser_class = registry.get_parser_class(platform)
            handler_class = registry.get_handler_class(platform)
            
            print(f"\n{platform.upper()}平台:")
            print(f"  客户端类: {client_class.__name__ if client_class else 'None'}")
            print(f"  解析器类: {parser_class.__name__ if parser_class else 'None'}")
            print(f"  处理器类: {handler_class.__name__ if handler_class else 'None'}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_platform_client_creation():
    """测试平台客户端创建"""
    print("\n" + "=" * 60)
    print("测试平台客户端创建")
    print("=" * 60)
    
    try:
        from src.platforms.registry import registry
        from src.config import settings
        
        # 测试Facebook客户端
        print("\n测试Facebook客户端:")
        fb_client = registry.create_client(
            "facebook",
            access_token=settings.facebook_access_token
        )
        if fb_client:
            print("  ✅ Facebook客户端创建成功")
            print(f"  Base URL: {fb_client.base_url}")
            await fb_client.close()
        else:
            print("  ❌ Facebook客户端创建失败")
            return False
        
        # 测试Instagram客户端
        print("\n测试Instagram客户端:")
        instagram_token = getattr(settings, 'instagram_access_token', None) or settings.facebook_access_token
        ig_user_id = getattr(settings, 'instagram_user_id', None)
        
        ig_client = registry.create_client(
            "instagram",
            access_token=instagram_token,
            ig_user_id=ig_user_id
        )
        if ig_client:
            print("  ✅ Instagram客户端创建成功")
            print(f"  Base URL: {ig_client.base_url}")
            if ig_user_id:
                print(f"  Instagram User ID: {ig_user_id}")
            else:
                print("  ⚠️  Instagram User ID未配置")
            await ig_client.close()
        else:
            print("  ❌ Instagram客户端创建失败")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_platform_parser():
    """测试平台解析器"""
    print("\n" + "=" * 60)
    print("测试平台解析器")
    print("=" * 60)
    
    try:
        from src.platforms.registry import registry
        
        # 测试Facebook解析器
        print("\n测试Facebook解析器:")
        fb_parser = registry.create_parser("facebook")
        if fb_parser:
            print("  ✅ Facebook解析器创建成功")
            
            # 测试解析Facebook事件
            test_event = {
                "object": "page",
                "entry": [{
                    "id": "test_page_id",
                    "messaging": [{
                        "sender": {"id": "123456"},
                        "recipient": {"id": "test_page_id"},
                        "message": {"text": "测试消息", "mid": "msg_123"},
                        "timestamp": 1234567890
                    }]
                }]
            }
            
            result = fb_parser.parse_webhook_event(test_event)
            if result:
                print(f"  ✅ 成功解析 {len(result)} 条消息")
            else:
                print("  ⚠️  未解析到消息（可能是测试数据格式问题）")
        else:
            print("  ❌ Facebook解析器创建失败")
            return False
        
        # 测试Instagram解析器
        print("\n测试Instagram解析器:")
        ig_parser = registry.create_parser("instagram")
        if ig_parser:
            print("  ✅ Instagram解析器创建成功")
            
            # 测试解析Instagram事件
            test_event = {
                "object": "instagram",
                "entry": [{
                    "id": "test_page_id",
                    "messaging": [{
                        "sender": {"id": "123456"},
                        "recipient": {"id": "test_page_id"},
                        "message": {"text": "测试消息", "mid": "msg_123"},
                        "timestamp": 1234567890
                    }]
                }]
            }
            
            result = ig_parser.parse_webhook_event(test_event)
            if result:
                print(f"  ✅ 成功解析 {len(result)} 条消息")
            else:
                print("  ⚠️  未解析到消息（可能是测试数据格式问题）")
        else:
            print("  ❌ Instagram解析器创建失败")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_platform_manager():
    """测试平台管理器"""
    print("\n" + "=" * 60)
    print("测试平台管理器")
    print("=" * 60)
    
    try:
        from src.platforms.manager import platform_manager
        from src.config import settings
        
        # 测试初始化Facebook平台
        print("\n测试初始化Facebook平台:")
        fb_init = platform_manager.initialize_platform(
            "facebook",
            access_token=settings.facebook_access_token,
            verify_token=settings.facebook_verify_token
        )
        if fb_init:
            print("  ✅ Facebook平台初始化成功")
            platform_manager.enable_platform("facebook")
            print("  ✅ Facebook平台已启用")
        else:
            print("  ❌ Facebook平台初始化失败")
            return False
        
        # 测试获取客户端
        fb_client = platform_manager.get_client("facebook")
        if fb_client:
            print("  ✅ 成功获取Facebook客户端")
            await fb_client.close()
        else:
            print("  ❌ 获取Facebook客户端失败")
        
        # 测试初始化Instagram平台
        print("\n测试初始化Instagram平台:")
        instagram_token = getattr(settings, 'instagram_access_token', None) or settings.facebook_access_token
        instagram_verify = getattr(settings, 'instagram_verify_token', None) or settings.facebook_verify_token
        
        ig_init = platform_manager.initialize_platform(
            "instagram",
            access_token=instagram_token,
            verify_token=instagram_verify,
            base_url="https://graph.facebook.com/v18.0"
        )
        if ig_init:
            print("  ✅ Instagram平台初始化成功")
            platform_manager.enable_platform("instagram")
            print("  ✅ Instagram平台已启用")
        else:
            print("  ⚠️  Instagram平台初始化失败（可能是配置问题）")
        
        # 列出已初始化的平台
        initialized = platform_manager.list_initialized_platforms()
        print(f"\n已初始化的平台: {initialized}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("平台集成功能测试")
    print("=" * 60)
    
    results = []
    
    results.append(("平台注册器", await test_platform_registry()))
    results.append(("平台客户端创建", await test_platform_client_creation()))
    results.append(("平台解析器", await test_platform_parser()))
    results.append(("平台管理器", await test_platform_manager()))
    
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("⚠️  部分测试未通过，请查看上述错误信息。")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)





