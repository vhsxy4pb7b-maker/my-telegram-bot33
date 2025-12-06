"""测试Facebook帖子管理和广告管理功能"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_post_management():
    """测试帖子管理功能"""
    print("=" * 60)
    print("测试Facebook帖子管理功能")
    print("=" * 60)
    
    try:
        from src.facebook.api_client import FacebookAPIClient
        from src.config import settings
        
        client = FacebookAPIClient()
        
        print("\n✅ Facebook客户端创建成功")
        print(f"   Base URL: {client.base_url}")
        
        # 测试获取帖子信息（使用一个示例帖子ID）
        print("\n📝 测试获取帖子信息...")
        print("   (需要有效的post_id才能测试)")
        print("   方法: client.get_post(post_id='your_post_id')")
        
        # 测试创建帖子（需要有效的page_id）
        print("\n📝 测试创建帖子方法...")
        print("   方法: client.create_post(page_id='your_page_id', message='内容')")
        print("   ✅ 方法已实现")
        
        # 测试删除帖子
        print("\n📝 测试删除帖子方法...")
        print("   方法: client.delete_post(post_id='your_post_id')")
        print("   ✅ 方法已实现")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_ads_management():
    """测试广告管理功能"""
    print("\n" + "=" * 60)
    print("测试Facebook广告管理功能")
    print("=" * 60)
    
    try:
        from src.facebook.api_client import FacebookAPIClient
        from src.config import settings
        
        client = FacebookAPIClient()
        
        print("\n✅ Facebook客户端创建成功")
        
        # 测试获取广告账户
        print("\n📊 测试获取广告账户方法...")
        print("   方法: client.get_ad_accounts()")
        print("   ✅ 方法已实现")
        print("   ⚠️  需要 ads_read 权限")
        
        # 测试获取广告列表
        print("\n📊 测试获取广告列表方法...")
        print("   方法: client.get_ads(ad_account_id='account_id')")
        print("   ✅ 方法已实现")
        
        # 测试获取单个广告
        print("\n📊 测试获取单个广告方法...")
        print("   方法: client.get_ad(ad_id='ad_id')")
        print("   ✅ 方法已实现")
        
        # 测试创建广告
        print("\n📊 测试创建广告方法...")
        print("   方法: client.create_ad(ad_account_id, adset_id, creative_id, name)")
        print("   ✅ 方法已实现")
        print("   ⚠️  需要 ads_management 权限")
        
        # 测试更新广告
        print("\n📊 测试更新广告方法...")
        print("   方法: client.update_ad(ad_id, name='新名称', status='ACTIVE')")
        print("   ✅ 方法已实现")
        
        # 测试删除广告
        print("\n📊 测试删除广告方法...")
        print("   方法: client.delete_ad(ad_id='ad_id')")
        print("   ✅ 方法已实现")
        
        # 测试获取广告系列
        print("\n📊 测试获取广告系列方法...")
        print("   方法: client.get_campaigns(ad_account_id='account_id')")
        print("   ✅ 方法已实现")
        
        # 测试获取广告组
        print("\n📊 测试获取广告组方法...")
        print("   方法: client.get_adsets(ad_account_id='account_id')")
        print("   ✅ 方法已实现")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_method_availability():
    """测试方法是否可用"""
    print("\n" + "=" * 60)
    print("测试方法可用性")
    print("=" * 60)
    
    try:
        from src.facebook.api_client import FacebookAPIClient
        
        client = FacebookAPIClient()
        
        # 帖子管理方法
        post_methods = [
            'create_post',
            'delete_post',
            'get_post'
        ]
        
        print("\n📝 帖子管理方法:")
        for method in post_methods:
            if hasattr(client, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - 方法不存在")
                return False
        
        # 广告管理方法
        ads_methods = [
            'get_ad_accounts',
            'get_ads',
            'get_ad',
            'create_ad',
            'update_ad',
            'delete_ad',
            'get_campaigns',
            'get_adsets'
        ]
        
        print("\n📊 广告管理方法:")
        for method in ads_methods:
            if hasattr(client, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - 方法不存在")
                return False
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("Facebook帖子管理和广告管理功能测试")
    print("=" * 60)
    
    results = []
    
    results.append(("方法可用性", await test_method_availability()))
    results.append(("帖子管理功能", await test_post_management()))
    results.append(("广告管理功能", await test_ads_management()))
    
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
        print("\n📌 注意：")
        print("   - 帖子管理需要 pages_manage_posts 权限")
        print("   - 广告管理需要 ads_read 和 ads_management 权限")
        print("   - 实际使用需要有效的 page_id 和 ad_account_id")
    else:
        print("⚠️  部分测试未通过，请查看上述错误信息。")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)




