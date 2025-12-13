"""检查Token过期时间并预警"""
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config.page_token_manager import page_token_manager
import asyncio
import httpx

# 预警天数（提前多少天预警）
WARNING_DAYS = 7

async def check_token_expiry(token: str) -> Dict[str, Any]:
    """
    检查Token过期时间
    
    Args:
        token: Facebook Access Token
    
    Returns:
        包含过期信息的字典
    """
    url = "https://graph.facebook.com/v18.0/debug_token"
    params = {
        "input_token": token,
        "access_token": token
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                token_info = data.get("data", {})
                
                expires_at = token_info.get("expires_at")
                is_valid = token_info.get("is_valid", False)
                
                result = {
                    "is_valid": is_valid,
                    "expires_at": expires_at,
                    "expires_at_datetime": None,
                    "days_until_expiry": None,
                    "is_expired": False,
                    "needs_warning": False
                }
                
                if expires_at:
                    # expires_at 是 Unix 时间戳
                    expires_datetime = datetime.fromtimestamp(expires_at, tz=timezone.utc)
                    result["expires_at_datetime"] = expires_datetime
                    
                    now = datetime.now(timezone.utc)
                    delta = expires_datetime - now
                    days = delta.days
                    
                    result["days_until_expiry"] = days
                    result["is_expired"] = days < 0
                    result["needs_warning"] = 0 <= days <= WARNING_DAYS
                
                return result
            else:
                return {
                    "is_valid": False,
                    "error": "无法检查Token状态"
                }
    except Exception as e:
        return {
            "is_valid": False,
            "error": str(e)
        }

async def check_all_tokens_async():
    """检查所有Token的过期时间（异步版本）"""
    tokens = page_token_manager._tokens
    pages = page_token_manager.list_pages()
    
    if not tokens:
        return []
    
    results = []
    
    async def check_token_async(page_id: str, token: str):
        page_info = pages.get(page_id, {})
        page_name = page_info.get("name", page_id)
        
        # 先检查配置中的过期时间
        config_expires_at = page_info.get("expires_at")
        
        # 检查Token实际过期时间
        token_info = await check_token_expiry(token)
        
        results.append({
            "page_id": page_id,
            "page_name": page_name,
            "token_info": token_info,
            "config_expires_at": config_expires_at
        })
    
    # 检查所有Token
    tasks = []
    for page_id, token in tokens.items():
        if page_id == "default":
            continue
        tasks.append(check_token_async(page_id, token))
    
    if tasks:
        await asyncio.gather(*tasks)
    
    return results

def check_all_tokens():
    """检查所有Token的过期时间"""
    print("=" * 70)
    print("检查Token过期时间")
    print("=" * 70)
    print()
    
    tokens = page_token_manager._tokens
    pages = page_token_manager.list_pages()
    
    if not tokens:
        print("⚠️  没有配置Token")
        return
    
    # 异步检查所有Token
    results = asyncio.run(check_all_tokens_async())
    
    # 显示结果
    print(f"{'页面名称':<30} {'状态':<10} {'剩余天数':<12} {'过期时间':<20} {'预警':<8}")
    print("-" * 80)
    
    expired_tokens = []
    warning_tokens = []
    valid_tokens = []
    
    for result in results:
        page_name = result["page_name"]
        token_info = result["token_info"]
        
        if not token_info.get("is_valid"):
            status = "❌ 无效"
            days = "N/A"
            expires_str = "N/A"
            warning = ""
            expired_tokens.append(result)
        elif token_info.get("is_expired"):
            status = "❌ 已过期"
            days = f"{token_info.get('days_until_expiry', 0)}"
            expires_str = token_info.get("expires_at_datetime", "").strftime("%Y-%m-%d %H:%M") if token_info.get("expires_at_datetime") else "N/A"
            warning = "⚠️"
            expired_tokens.append(result)
        elif token_info.get("needs_warning"):
            status = "⚠️ 即将过期"
            days = f"{token_info.get('days_until_expiry', 0)}"
            expires_str = token_info.get("expires_at_datetime", "").strftime("%Y-%m-%d %H:%M") if token_info.get("expires_at_datetime") else "N/A"
            warning = "⚠️"
            warning_tokens.append(result)
        else:
            status = "✅ 正常"
            days = f"{token_info.get('days_until_expiry', 'N/A')}"
            expires_str = token_info.get("expires_at_datetime", "").strftime("%Y-%m-%d %H:%M") if token_info.get("expires_at_datetime") else "N/A"
            warning = ""
            valid_tokens.append(result)
        
        print(f"{page_name:<30} {status:<10} {days:<12} {expires_str:<20} {warning:<8}")
    
    print()
    print("=" * 70)
    print()
    
    # 汇总
    if expired_tokens:
        print(f"❌ 已过期的Token：{len(expired_tokens)} 个")
        for result in expired_tokens:
            print(f"   - {result['page_name']} ({result['page_id']})")
        print()
    
    if warning_tokens:
        print(f"⚠️  需要预警的Token（{WARNING_DAYS}天内过期）：{len(warning_tokens)} 个")
        for result in warning_tokens:
            days = result['token_info'].get('days_until_expiry', 0)
            print(f"   - {result['page_name']} ({result['page_id']}) - 还有 {days} 天过期")
        print()
    
    if valid_tokens:
        print(f"✅ 正常的Token：{len(valid_tokens)} 个")
    
    print()
    print("💡 建议：")
    if expired_tokens or warning_tokens:
        print("   请运行以下命令更新Token：")
        print("   python scripts/tools/convert_to_long_lived_token.py")
    else:
        print("   所有Token状态正常，无需更新")
    print()

if __name__ == "__main__":
    check_all_tokens()

