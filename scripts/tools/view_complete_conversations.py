"""查看完整的对话记录"""
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import desc

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.database import SessionLocal
from src.database.models import Conversation, Customer

def view_complete_conversations():
    """查看完整的对话记录"""
    db = SessionLocal()
    try:
        # 统计信息
        total = db.query(Conversation).count()
        replied = db.query(Conversation).filter(Conversation.ai_replied == True).count()
        with_reply = db.query(Conversation).filter(Conversation.ai_reply_content.isnot(None)).count()
        
        print("=" * 70)
        print("完整对话记录统计")
        print("=" * 70)
        print(f"总对话数: {total}")
        print(f"已回复数: {replied}")
        print(f"有回复内容数: {with_reply}")
        print()
        
        # 查看最近5条完整对话
        print("=" * 70)
        print("最近5条完整对话记录")
        print("=" * 70)
        print()
        
        convs = db.query(Conversation)\
            .filter(
                Conversation.ai_replied == True,
                Conversation.ai_reply_content.isnot(None)
            )\
            .order_by(desc(Conversation.created_at))\
            .limit(5)\
            .all()
        
        if not convs:
            print("❌ 没有找到完整的对话记录")
            return
        
        for idx, conv in enumerate(convs, 1):
            customer = db.query(Customer).filter(Customer.id == conv.customer_id).first()
            customer_name = customer.name if customer else f"客户ID: {conv.customer_id}"
            
            print(f"对话 #{idx} (ID: {conv.id})")
            print(f"客户: {customer_name}")
            print(f"时间: {conv.created_at}")
            print(f"平台: {conv.platform.value}")
            print()
            print("📨 客户消息:")
            print(f"   {conv.content[:200]}{'...' if len(conv.content) > 200 else ''}")
            print()
            print("🤖 AI回复:")
            print(f"   {conv.ai_reply_content[:200]}{'...' if len(conv.ai_reply_content) > 200 else ''}")
            print()
            print("-" * 70)
            print()
        
        # 查看某个客户的多轮对话
        print("=" * 70)
        print("客户多轮对话序列")
        print("=" * 70)
        print()
        
        # 找出有最多对话的客户
        from sqlalchemy import func
        customer_convs = db.query(
            Conversation.customer_id,
            func.count(Conversation.id).label('conv_count')
        )\
        .filter(Conversation.ai_replied == True)\
        .group_by(Conversation.customer_id)\
        .order_by(desc('conv_count'))\
        .limit(3)\
        .all()
        
        if customer_convs:
            for customer_id, conv_count in customer_convs:
                customer = db.query(Customer).filter(Customer.id == customer_id).first()
                customer_name = customer.name if customer else f"客户ID: {customer_id}"
                
                print(f"客户: {customer_name} (ID: {customer_id})")
                print(f"对话轮数: {conv_count}")
                print()
                
                # 获取该客户的所有对话，按时间排序
                customer_conversations = db.query(Conversation)\
                    .filter(
                        Conversation.customer_id == customer_id,
                        Conversation.ai_replied == True
                    )\
                    .order_by(Conversation.created_at)\
                    .all()
                
                for i, conv in enumerate(customer_conversations, 1):
                    print(f"  轮次 {i} - {conv.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"    客户: {conv.content[:100]}{'...' if len(conv.content) > 100 else ''}")
                    if conv.ai_reply_content:
                        print(f"    AI: {conv.ai_reply_content[:100]}{'...' if len(conv.ai_reply_content) > 100 else ''}")
                    print()
                
                print("-" * 70)
                print()
        else:
            print("❌ 没有找到多轮对话的客户")
        
        # 检查是否有未回复的对话
        unreplied = db.query(Conversation)\
            .filter(Conversation.ai_replied == False)\
            .count()
        
        if unreplied > 0:
            print("=" * 70)
            print(f"⚠️  发现 {unreplied} 条未回复的对话")
            print("=" * 70)
            print()
            
            unreplied_convs = db.query(Conversation)\
                .filter(Conversation.ai_replied == False)\
                .order_by(desc(Conversation.created_at))\
                .limit(5)\
                .all()
            
            for conv in unreplied_convs:
                customer = db.query(Customer).filter(Customer.id == conv.customer_id).first()
                customer_name = customer.name if customer else f"客户ID: {conv.customer_id}"
                print(f"对话ID: {conv.id}, 客户: {customer_name}")
                print(f"消息: {conv.content[:100]}{'...' if len(conv.content) > 100 else ''}")
                print(f"时间: {conv.created_at}")
                print()
        
    finally:
        db.close()

if __name__ == "__main__":
    try:
        view_complete_conversations()
    except Exception as e:
        print(f"❌ 查看对话记录时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

