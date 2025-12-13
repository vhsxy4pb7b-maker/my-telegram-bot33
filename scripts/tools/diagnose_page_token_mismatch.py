"""诊断页面Token不匹配问题"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import httpx
from src.config.page_token_manager import page_token_manager
from src.config.page_settings import page_settings

async def check_page_token(page_id: str, token: str) -> dict:
    """检查页面Token是否有效"""
    result = {
        "page_id": page_id,
        "token_valid": False,
        "token_page_id": None,
        "error": None,
        "permissions": []
    }
    
    try:
        # 检查Token信息
        async with httpx.AsyncClient() as client:
            # 获取Token信息
            debug_url = f"https://graph.facebook.com/v18.0/debug_token"
            params = {
                "input_token": token,
                "access_token": token
            }
            
            response = await client.get(debug_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                token_data = data.get("data", {})
                
                result["token_valid"] = token_data.get("is_valid", False)
                result["token_page_id"] = token_data.get("profile_id")
                
                # 检查权限
                scopes = token_data.get("scopes", [])
                result["permissions"] = scopes
                
                # 检查页面ID是否匹配
                if result["token_page_id"] != page_id:
                    result["error"] = f"Token belongs to page {result['token_page_id']}, but configured for page {page_id}"
                else:
                    result["error"] = None
            else:
                error_data = response.json()
                error_info = error_data.get("error", {})
                result["error"] = f"{error_info.get('message', 'Unknown error')} (code: {error_info.get('code')})"
                
    except Exception as e:
        result["error"] = f"Exception: {str(e)}"
    
    return result

async def diagnose_all_pages():
    """诊断所有页面的Token"""
    print("=" * 70)
    print("页面Token诊断工具")
    print("=" * 70)
    print()
    
    pages = page_token_manager.list_pages()
    
    if not pages:
        print("❌ 没有配置任何页面")
        return
    
    print(f"找到 {len(pages)} 个配置的页面")
    print()
    
    results = []
    
    for page_id, page_info in pages.items():
        if page_id == "default":
            continue
        
        token = page_token_manager.get_token(page_id)
        page_name = page_info.get("name", "未知")
        
        print(f"检查页面: {page_name} (ID: {page_id})")
        print("-" * 70)
        
        if not token:
            print("  ❌ Token未配置")
            results.append({
                "page_id": page_id,
                "page_name": page_name,
                "status": "no_token",
                "error": "Token未配置"
            })
        else:
            result = await check_page_token(page_id, token)
            results.append({
                "page_id": page_id,
                "page_name": page_name,
                "status": "mismatch" if result["error"] else "ok",
                **result
            })
            
            if result["token_valid"]:
                if result["token_page_id"] == page_id:
                    print(f"  ✅ Token有效且匹配")
                    print(f"  ✅ 页面ID: {result['token_page_id']}")
                else:
                    print(f"  ❌ Token有效但不匹配")
                    print(f"  ⚠️  Token属于页面: {result['token_page_id']}")
                    print(f"  ⚠️  配置的页面ID: {page_id}")
                    print(f"  ❌ 错误: {result['error']}")
            else:
                print(f"  ❌ Token无效")
                if result["error"]:
                    print(f"  ❌ 错误: {result['error']}")
            
            if result["permissions"]:
                print(f"  📋 权限: {', '.join(result['permissions'])}")
        
        print()
        await asyncio.sleep(0.5)  # 避免API速率限制
    
    # 总结
    print("=" * 70)
    print("诊断总结")
    print("=" * 70)
    print()
    
    ok_count = sum(1 for r in results if r["status"] == "ok")
    mismatch_count = sum(1 for r in results if r["status"] == "mismatch")
    no_token_count = sum(1 for r in results if r["status"] == "no_token")
    
    print(f"✅ 正常: {ok_count} 个页面")
    print(f"❌ Token不匹配: {mismatch_count} 个页面")
    print(f"⚠️  Token未配置: {no_token_count} 个页面")
    print()
    
    if mismatch_count > 0:
        print("需要修复的页面:")
        print()
        for r in results:
            if r["status"] == "mismatch":
                print(f"  - {r['page_name']} (ID: {r['page_id']})")
                print(f"    Token属于页面: {r.get('token_page_id', 'N/A')}")
                print(f"    建议: 使用正确的页面Token更新")
                print()
        
        print("修复方法:")
        print("  1. 访问 https://developers.facebook.com/tools/debug/accesstoken/")
        print("  2. 输入Token检查其所属页面")
        print("  3. 获取正确的页面Token")
        print("  4. 运行: python scripts/tools/manage_pages.py")
        print("  5. 或直接更新 .page_tokens.json 文件")
        print()
    
    if no_token_count > 0:
        print("需要配置Token的页面:")
        for r in results:
            if r["status"] == "no_token":
                print(f"  - {r['page_name']} (ID: {r['page_id']})")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(diagnose_all_pages())
    except Exception as e:
        print(f"❌ 诊断过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

