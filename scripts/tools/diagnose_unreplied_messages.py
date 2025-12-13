"""诊断未回复消息问题"""
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.database import SessionLocal
from src.database.models import Conversation, Customer
from sqlalchemy import and_, func

def diagnose():
    """诊断未回复消息问题"""
    db = SessionLocal()
    
    print("=" * 80)
    print("未回复消息诊断")
    print("=" * 80)
    print()
    
    try:
        # 1. 检查总对话数
        total = db.query(Conversation).count()
        print(f"1. 总对话数: {total}")
        print()
        
        if total == 0:
            print("⚠️  数据库中没有对话记录！")
            print()
            print("可能的原因：")
            print("  - 消息没有被保存到数据库")
            print("  - Webhook没有接收到消息")
            print("  - 消息处理流程中断")
            print()
            print("建议检查：")
            print("  - 查看日志文件 logs/app.log")
            print("  - 检查Webhook是否正常接收消息")
            print("  - 检查消息处理流程是否正常")
            return
        
        # 2. 检查时间分布
        earliest = db.query(func.min(Conversation.received_at)).scalar()
        latest = db.query(func.max(Conversation.received_at)).scalar()
        print(f"2. 时间范围:")
        print(f"   最早: {earliest}")
        print(f"   最新: {latest}")
        print()
        
        # 3. 检查回复状态
        replied = db.query(Conversation).filter(Conversation.ai_replied == True).count()
        unreplied = db.query(Conversation).filter(Conversation.ai_replied == False).count()
        print(f"3. 回复状态:")
        print(f"   已回复: {replied}")
        print(f"   未回复: {unreplied}")
        print()
        
        # 4. 检查过滤状态
        filtered = db.query(Conversation).filter(Conversation.filtered == True).count()
        not_filtered = db.query(Conversation).filter(Conversation.filtered == False).count()
        print(f"4. 过滤状态:")
        print(f"   已过滤: {filtered}")
        print(f"   未过滤: {not_filtered}")
        print()
        
        # 5. 检查12月13日后的消息
        start_date = datetime(2025, 12, 13, 0, 0, 0, tzinfo=timezone.utc)
        recent_total = db.query(Conversation).filter(
            Conversation.received_at >= start_date
        ).count()
        recent_unreplied = db.query(Conversation).filter(
            and_(
                Conversation.received_at >= start_date,
                Conversation.ai_replied == False,
                Conversation.filtered == False
            )
        ).count()
        recent_replied = db.query(Conversation).filter(
            and_(
                Conversation.received_at >= start_date,
                Conversation.ai_replied == True
            )
        ).count()
        print(f"5. 12月13日后的消息:")
        print(f"   总数: {recent_total}")
        print(f"   已回复: {recent_replied}")
        print(f"   未回复（未过滤）: {recent_unreplied}")
        print()
        
        # 6. 检查超过5分钟未回复的消息
        now = datetime.now(timezone.utc)
        five_min_ago = now - timedelta(minutes=5)
        old_unreplied = db.query(Conversation).filter(
            and_(
                Conversation.received_at >= start_date,
                Conversation.received_at <= five_min_ago,
                Conversation.ai_replied == False,
                Conversation.filtered == False
            )
        ).count()
        print(f"6. 超过5分钟未回复的消息（12月13日后）: {old_unreplied}")
        print()
        
        # 7. 显示最近的未回复消息
        print("7. 最近的未回复消息（前10条）:")
        unreplied_messages = db.query(Conversation).filter(
            Conversation.ai_replied == False
        ).order_by(Conversation.received_at.desc()).limit(10).all()
        
        if unreplied_messages:
            print(f"{'ID':<8} {'时间':<20} {'过滤':<8} {'内容预览':<50}")
            print("-" * 90)
            for conv in unreplied_messages:
                time_str = conv.received_at.strftime('%Y-%m-%d %H:%M:%S') if conv.received_at else 'N/A'
                content = (conv.content[:47] + '..') if conv.content and len(conv.content) > 50 else (conv.content or 'N/A')
                filtered_str = '是' if conv.filtered else '否'
                print(f"{conv.id:<8} {time_str:<20} {filtered_str:<8} {content:<50}")
        else:
            print("   没有未回复的消息")
        print()
        
        # 8. 检查产品关键词
        product_keywords = [
            "iphone", "ip", "苹果", "apple", "loan", "borrow", "lend", "贷款", "借款", 
            "借", "贷", "price", "cost", "费用", "价格", "多少钱", "interest", "利息",
            "model", "型号", "容量", "storage", "apple id", "id card", "身份证",
            "咨询", "了解", "询问", "办理", "申请", "apply", "怎么", "如何", "how",
            "服务", "service", "客服", "customer service", "legit", "legitimate", 
            "真实", "真的", "可靠", "reliable", "可信", "?", "？"
        ]
        
        print("8. 检查产品关键词匹配:")
        product_unreplied = []
        for conv in unreplied_messages:
            if conv.content:
                content_lower = conv.content.lower()
                if any(keyword in content_lower for keyword in product_keywords):
                    product_unreplied.append(conv)
        
        print(f"   未回复消息中包含产品关键词的: {len(product_unreplied)} 条")
        if product_unreplied:
            print("   这些消息应该被自动回复:")
            for conv in product_unreplied[:5]:
                print(f"     - ID {conv.id}: {conv.content[:60]}...")
        print()
        
        # 9. 诊断建议
        print("=" * 80)
        print("诊断建议")
        print("=" * 80)
        print()
        
        if total == 0:
            print("❌ 问题：数据库中没有对话记录")
            print("   建议：检查消息是否被正确接收和处理")
        elif recent_unreplied > 0:
            print(f"⚠️  发现 {recent_unreplied} 条未回复的消息（12月13日后）")
            if old_unreplied > 0:
                print(f"   ⚠️  其中 {old_unreplied} 条超过5分钟未回复")
                print("   建议：检查自动回复调度器是否正常运行")
            if len(product_unreplied) > 0:
                print(f"   ⚠️  其中 {len(product_unreplied)} 条包含产品关键词，应该被自动回复")
                print("   建议：检查自动回复调度器的扫描逻辑")
        else:
            print("✅ 没有发现未回复的消息")
        
        print()
        
    except Exception as e:
        print(f"❌ 诊断过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    diagnose()

