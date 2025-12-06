"""检查Facebook访问令牌的权限"""
import sys
import os
import httpx
import asyncio
from typing import Dict, List, Optional, Any

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# 定义所需权限
REQUIRED_PERMISSIONS = {
    "基础权限": [
        "pages_messaging",
        "pages_read_engagement",
        "pages_manage_metadata"
    ],
    "帖子管理": [
        "pages_manage_posts"
    ],
    "广告管理": [
        "ads_read",
        "ads_management"
    ]
}


async def check_permissions(access_token: str) -> bool:
    """检查访问令牌的权限"""
    print("=" * 60)
    print("检查Facebook访问令牌权限")
    print("=" * 60)
    
    base_url = "https://graph.facebook.com/v18.0"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 获取权限列表
        try:
            url = f"{base_url}/me/permissions"
            params = {"access_token": access_token}
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            permissions: List[Dict[str, Any]] = data.get("data", [])
            
            print(f"\n当前令牌的权限数量: {len(permissions)}")
            print("\n权限列表:")
            print("-" * 60)
            
            # 检查每个权限
            granted_permissions: Dict[str, bool] = {}
            for perm in permissions:
                perm_name = perm.get("permission", "unknown")
                status = perm.get("status", "unknown")
                granted_permissions[perm_name] = status == "granted"
                
                status_icon = "✅" if status == "granted" else "❌"
                print(f"{status_icon} {perm_name}: {status}")
            
            # 检查所需权限
            print("\n" + "=" * 60)
            print("权限检查结果")
            print("=" * 60)
            
            all_granted = True
            
            for category, perms in REQUIRED_PERMISSIONS.items():
                print(f"\n{category}:")
                for perm in perms:
                    if perm in granted_permissions:
                        if granted_permissions[perm]:
                            print(f"  ✅ {perm} - 已授予")
                        else:
                            print(f"  ❌ {perm} - 未授予")
                            all_granted = False
                    else:
                        print(f"  ⚠️  {perm} - 未找到")
                        all_granted = False
            
            # 检查令牌信息
            print("\n" + "=" * 60)
            print("令牌信息")
            print("=" * 60)
            
            try:
                debug_url = f"{base_url}/debug_token"
                debug_params = {
                    "input_token": access_token,
                    "access_token": access_token
                }
                
                debug_response = await client.get(debug_url, params=debug_params)
                debug_response.raise_for_status()
                debug_data = debug_response.json().get("data", {})
                
                print(f"应用ID: {debug_data.get('app_id')}")
                print(f"用户ID: {debug_data.get('user_id')}")
                print(f"类型: {debug_data.get('type')}")
                print(f"过期时间: {debug_data.get('expires_at', 0)}")
                
                scopes = debug_data.get("scopes", [])
                if scopes:
                    print(f"权限范围: {', '.join(scopes)}")
                
            except Exception as e:
                print(f"⚠️  无法获取令牌详细信息: {str(e)}")
            
            return all_granted
            
        except httpx.HTTPStatusError as e:
            print(f"❌ API请求失败: {e.response.status_code}")
            print(f"错误信息: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ 检查失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


async def test_post_permission(access_token: str, page_id: Optional[str] = None) -> bool:
    """测试帖子管理权限"""
    print("\n" + "=" * 60)
    print("测试帖子管理权限")
    print("=" * 60)
    
    if not page_id:
        print("⚠️  未提供page_id，跳过实际测试")
        return True
    
    try:
        from src.facebook.api_client import FacebookAPIClient
        
        client = FacebookAPIClient(access_token=access_token)
        
        # 尝试获取页面信息（测试基本权限）
        print("\n测试获取页面信息...")
        page_info = await client.get_user_info(page_id)
        print(f"✅ 页面信息获取成功: {page_info.get('name', 'N/A')}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


async def test_ads_permission(access_token: str) -> bool:
    """测试广告管理权限"""
    print("\n" + "=" * 60)
    print("测试广告管理权限")
    print("=" * 60)
    
    try:
        from src.facebook.api_client import FacebookAPIClient
        
        client = FacebookAPIClient(access_token=access_token)
        
        # 尝试获取广告账户（测试ads_read权限）
        print("\n测试获取广告账户...")
        try:
            accounts = await client.get_ad_accounts()
            if accounts.get("data"):
                print(f"✅ ads_read权限正常，找到 {len(accounts['data'])} 个广告账户")
            else:
                print("⚠️  ads_read权限正常，但没有广告账户")
        except Exception as e:
            print(f"❌ ads_read权限不足: {str(e)}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


async def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Facebook权限检查工具")
    print("=" * 60)
    
    # 从环境变量或配置文件获取访问令牌
    try:
        from src.config import settings
        access_token = settings.facebook_access_token
    except Exception as e:
        print(f"❌ 无法获取访问令牌: {str(e)}")
        print("\n请确保已配置FACEBOOK_ACCESS_TOKEN环境变量")
        return 1
    
    if not access_token:
        print("❌ 访问令牌未配置")
        print("\n请在.env文件中配置FACEBOOK_ACCESS_TOKEN")
        return 1
    
    print(f"\n使用访问令牌: {access_token[:20]}...")
    
    # 检查权限
    permissions_ok = await check_permissions(access_token)
    
    # 测试功能权限（可选）
    if len(sys.argv) > 1:
        if "--test-post" in sys.argv:
            try:
                post_index = sys.argv.index("--test-post")
                page_id = sys.argv[post_index + 1] if len(sys.argv) > post_index + 1 else None
            except (ValueError, IndexError):
                page_id = None
            await test_post_permission(access_token, page_id)
        
        if "--test-ads" in sys.argv:
            await test_ads_permission(access_token)
    
    print("\n" + "=" * 60)
    if permissions_ok:
        print("✅ 所有必需权限已授予")
    else:
        print("⚠️  部分权限未授予，请参考FACEBOOK_PERMISSIONS_GUIDE.md配置权限")
    print("=" * 60)
    
    return 0 if permissions_ok else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


