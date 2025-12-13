"""立即更新所有Token为新的长期Token"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.tools.convert_to_long_lived_token import convert_all_tokens_to_long_lived

if __name__ == "__main__":
    print("=" * 70)
    print("立即更新所有Token为长期Token")
    print("=" * 70)
    print()
    print("正在更新所有Token...")
    print()
    
    asyncio.run(convert_all_tokens_to_long_lived())
    
    print()
    print("=" * 70)
    print("✅ Token更新完成！")
    print("=" * 70)
    print()
    print("📋 下一步：")
    print("  1. 检查Token状态：")
    print("     python scripts/tools/check_token_expiry.py")
    print()
    print("  2. 重启服务：")
    print("     - 停止当前服务（Ctrl+C）")
    print("     - 重新运行：python run.py")
    print()
    print("=" * 70)

