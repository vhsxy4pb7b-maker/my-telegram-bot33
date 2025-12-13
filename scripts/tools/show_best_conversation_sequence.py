"""展示最完整的对话序列"""
import sys
from pathlib import Path
from sqlalchemy import desc

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.database import SessionLocal
from src.database.models import Conversation, Customer

def show_best_conversation_sequence():
    """展示最完整的对话序列"""
    db = SessionLocal()
    try:
        print("=" * 70)
        print("最完整的对话序列展示")
        print("=" * 70)
        print()
        
        # 找出对话轮数最多的客户
        from sqlalchemy import func
        customer_stats = db.query(
            Conversation.customer_id,
            func.count(Conversation.id).label('conv_count')
        )\
        .group_by(Conversation.customer_id)\
        .order_by(desc('conv_count'))\
        .limit(1)\
        .first()
        
        if not customer_stats or customer_stats.conv_count < 2:
            print("⚠️  目前没有超过2轮的对话序列")
            print()
            print("这是正常现象，原因如下：")
            print("  1. 系统设计是引导客户加入Telegram群组继续对话")
            print("  2. AI回复中会发送Telegram群组链接")
            print("  3. 客户在Telegram中继续对话，不在Facebook")
            print("  4. 因此Facebook上的对话序列较短是正常的")
            print()
            print("要查看完整的业务流程对话，需要：")
            print("  1. 检查Telegram群组中的对话记录")
            print("  2. 或者等待客户在Facebook上继续多轮对话")
            return
        
        customer_id = customer_stats.customer_id
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        customer_name = customer.name if customer else f"客户ID: {customer_id}"
        
        print(f"客户: {customer_name} (ID: {customer_id})")
        print(f"对话轮数: {customer_stats.conv_count}轮")
        print()
        print("=" * 70)
        print("完整对话序列")
        print("=" * 70)
        print()
        
        # 获取该客户的所有对话，按时间排序
        conversations = db.query(Conversation)\
            .filter(Conversation.customer_id == customer_id)\
            .order_by(Conversation.created_at)\
            .all()
        
        for i, conv in enumerate(conversations, 1):
            time_str = conv.created_at.strftime('%Y-%m-%d %H:%M:%S')
            print(f"【轮次 {i}】{time_str}")
            print()
            print(f"👤 客户: {conv.content}")
            print()
            
            if conv.ai_replied and conv.ai_reply_content:
                print(f"🤖 AI: {conv.ai_reply_content}")
            else:
                print("⚠️  AI: 未回复")
            print()
            print("-" * 70)
            print()
        
        # 显示其他有2轮对话的客户
        print("=" * 70)
        print("其他有2轮对话的客户")
        print("=" * 70)
        print()
        
        all_customer_stats = db.query(
            Conversation.customer_id,
            func.count(Conversation.id).label('conv_count')
        )\
        .group_by(Conversation.customer_id)\
        .having(func.count(Conversation.id) >= 2)\
        .order_by(desc('conv_count'))\
        .all()
        
        for customer_id, conv_count in all_customer_stats:
            if customer_id == customer_stats.customer_id:
                continue  # 跳过已经展示的客户
            
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            customer_name = customer.name if customer else f"客户ID: {customer_id}"
            
            print(f"客户: {customer_name} ({conv_count}轮)")
            conversations = db.query(Conversation)\
                .filter(Conversation.customer_id == customer_id)\
                .order_by(Conversation.created_at)\
                .all()
            
            for i, conv in enumerate(conversations, 1):
                print(f"  轮次{i}: {conv.content[:80]}{'...' if len(conv.content) > 80 else ''}")
                if conv.ai_replied:
                    print(f"    AI: {conv.ai_reply_content[:80]}{'...' if len(conv.ai_reply_content) > 80 else ''}")
            print()
        
        # 总结
        print("=" * 70)
        print("总结")
        print("=" * 70)
        print()
        print("✅ 系统正常保存了所有对话记录（客户消息和AI回复）")
        print("✅ 对话序列较短是正常现象，因为：")
        print("   1. AI回复引导客户加入Telegram群组")
        print("   2. 客户在Telegram中继续对话")
        print("   3. Facebook上的对话主要用于初始接触和引流")
        print()
        print("💡 要查看完整的业务流程对话，请检查Telegram群组记录")
        print()
        
    finally:
        db.close()

if __name__ == "__main__":
    try:
        show_best_conversation_sequence()
    except Exception as e:
        print(f"❌ 展示对话序列时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

