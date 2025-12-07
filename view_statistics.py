"""查看统计数据工具"""
import sys
import os
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.database import SessionLocal
from src.statistics.tracker import StatisticsTracker


def print_daily_stats(stats: dict):
    """打印每日统计数据"""
    print("\n" + "=" * 60)
    print(f"📊 {stats['date']} 统计数据")
    print("=" * 60)
    
    print(f"\n👥 接待统计:")
    print(f"  总接待客户数: {stats['total_customers']}")
    print(f"  新客户数: {stats['new_customers']}")
    print(f"  回头客数: {stats['returning_customers']}")
    
    print(f"\n💬 消息统计:")
    print(f"  总消息数: {stats['total_messages']}")
    
    print(f"\n📢 引流统计:")
    print(f"  发送群组邀请: {stats['group_invitations_sent']}")
    print(f"  成功引流数: {stats['successful_leads']}")
    print(f"  引流转化率: {stats['lead_conversion_rate']}")
    
    print(f"\n💰 开单统计:")
    print(f"  总开单数: {stats['total_orders']}")
    print(f"  成功开单数: {stats['successful_orders']}")
    print(f"  开单转化率: {stats['order_conversion_rate']}")
    
    if stats.get('frequent_questions'):
        print(f"\n❓ 高频问题:")
        for question, count in list(stats['frequent_questions'].items())[:5]:
            print(f"  - {question}: {count}次")


def print_frequent_questions(questions: list):
    """打印高频问题"""
    print("\n" + "=" * 60)
    print("❓ 高频问题 TOP 20")
    print("=" * 60)
    
    if not questions:
        print("\n暂无高频问题记录")
        return
    
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['question']}")
        print(f"   分类: {q['category'] or '未分类'}")
        print(f"   出现次数: {q['count']}")
        if q.get('sample_responses'):
            print(f"   示例回复: {q['sample_responses'][0].get('response', 'N/A')[:100]}...")


def main():
    """主函数"""
    db = SessionLocal()
    tracker = StatisticsTracker(db)
    
    print("=" * 60)
    print("📊 统计数据查看工具")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 查看今日统计")
        print("2. 查看指定日期统计")
        print("3. 查看最近7天统计")
        print("4. 查看高频问题")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            # 今日统计
            stats = tracker.get_daily_statistics()
            print_daily_stats(stats)
        
        elif choice == "2":
            # 指定日期
            date_str = input("请输入日期 (YYYY-MM-DD): ").strip()
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                stats = tracker.get_daily_statistics(target_date)
                print_daily_stats(stats)
            except ValueError:
                print("❌ 日期格式错误，请使用 YYYY-MM-DD 格式")
        
        elif choice == "3":
            # 最近7天
            print("\n最近7天统计汇总:")
            print("-" * 60)
            
            total_customers = 0
            total_messages = 0
            total_leads = 0
            total_orders = 0
            
            for i in range(6, -1, -1):
                target_date = date.today() - timedelta(days=i)
                stats = tracker.get_daily_statistics(target_date)
                
                print(f"\n{stats['date']}:")
                print(f"  客户: {stats['total_customers']} | "
                      f"消息: {stats['total_messages']} | "
                      f"引流: {stats['successful_leads']} | "
                      f"开单: {stats['successful_orders']}")
                
                total_customers += stats['total_customers']
                total_messages += stats['total_messages']
                total_leads += stats['successful_leads']
                total_orders += stats['successful_orders']
            
            print("\n" + "-" * 60)
            print(f"7天汇总:")
            print(f"  总客户: {total_customers}")
            print(f"  总消息: {total_messages}")
            print(f"  总引流: {total_leads}")
            print(f"  总开单: {total_orders}")
            if total_leads > 0:
                print(f"  开单转化率: {(total_orders / total_leads * 100):.1f}%")
        
        elif choice == "4":
            # 高频问题
            limit = input("显示数量 (默认20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            
            questions = tracker.get_frequent_questions(limit)
            print_frequent_questions(questions)
        
        elif choice == "5":
            print("\n再见！")
            break
        
        else:
            print("❌ 无效选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    finally:
        db.close()


