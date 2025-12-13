"""修复页面Token不匹配问题"""
import sys
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config.page_token_manager import page_token_manager

def fix_token_mismatch():
    """修复Token不匹配问题"""
    print("=" * 70)
    print("修复页面Token不匹配")
    print("=" * 70)
    print()
    
    # 读取当前Token配置
    token_file = project_root / ".page_tokens.json"
    
    if not token_file.exists():
        print("❌ Token配置文件不存在: .page_tokens.json")
        return
    
    with open(token_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tokens = data.get("tokens", {})
    page_info = data.get("page_info", {})
    
    # 根据诊断结果，交换这两个页面的Token
    page_732287 = "732287003311432"
    page_849418 = "849418138246708"
    
    if page_732287 not in tokens or page_849418 not in tokens:
        print("❌ 找不到需要修复的页面Token")
        return
    
    print("发现Token不匹配:")
    print(f"  页面 {page_732287} 的Token属于页面 {page_849418}")
    print(f"  页面 {page_849418} 的Token属于页面 {page_732287}")
    print()
    
    # 交换Token
    temp_token = tokens[page_732287]
    tokens[page_732287] = tokens[page_849418]
    tokens[page_849418] = temp_token
    
    print("正在交换Token...")
    
    # 保存更新后的配置
    data["tokens"] = tokens
    
    # 备份原文件
    backup_file = token_file.with_suffix('.json.backup')
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ 已备份原配置到: {backup_file}")
    
    # 保存新配置
    with open(token_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Token已交换")
    print()
    
    # 重新加载配置
    page_token_manager._load_tokens()
    
    print("验证修复结果:")
    print(f"  页面 {page_732287}: Token长度 {len(tokens[page_732287])} 字符")
    print(f"  页面 {page_849418}: Token长度 {len(tokens[page_849418])} 字符")
    print()
    print("⚠️  请运行诊断工具验证修复结果:")
    print("   python scripts/tools/diagnose_page_token_mismatch.py")
    print()
    print("💡 如果问题仍然存在，请:")
    print("   1. 访问 https://developers.facebook.com/tools/debug/accesstoken/")
    print("   2. 检查每个Token的实际所属页面")
    print("   3. 获取正确的页面Token")
    print("   4. 使用 manage_pages.py 更新Token")

if __name__ == "__main__":
    try:
        fix_token_mismatch()
    except Exception as e:
        print(f"❌ 修复过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

