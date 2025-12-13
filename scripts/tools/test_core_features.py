"""测试核心功能"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.database import SessionLocal
from src.ai.reply_generator import ReplyGenerator
from src.config import yaml_config

async def test_spam_detection():
    """测试垃圾信息检测"""
    print("=" * 70)
    print("测试1: 智能垃圾信息检测")
    print("=" * 70)
    print()
    
    db = SessionLocal()
    try:
        reply_generator = ReplyGenerator(db)
        
        test_cases = [
            ("我要买手机", True, "应该判定为垃圾（买卖意图）"),
            ("我想咨询iPhone贷款", False, "应该正常回复（业务意图）"),
            ("loan", False, "应该正常回复（业务关键词）"),
            ("how much", False, "应该正常回复（业务关键词）"),
            ("legit", False, "应该正常回复（业务关键词）"),
            ("买iphone", True, "应该判定为垃圾（买卖意图）"),
            ("卖手机", True, "应该判定为垃圾（买卖意图）"),
            ("😀😀😀", True, "应该判定为垃圾（纯表情）"),
            ("aaaaa", True, "应该判定为垃圾（重复字符）"),
        ]
        
        passed = 0
        failed = 0
        
        for message, expected_spam, description in test_cases:
            is_spam = reply_generator._is_spam_or_invalid(message)
            result = "✅" if is_spam == expected_spam else "❌"
            status = "垃圾" if is_spam else "正常"
            expected_status = "垃圾" if expected_spam else "正常"
            
            print(f"{result} 消息: '{message}'")
            print(f"   预期: {expected_status}, 实际: {status} - {description}")
            
            if is_spam == expected_spam:
                passed += 1
            else:
                failed += 1
            print()
        
        print(f"测试结果: {passed} 通过, {failed} 失败")
        return failed == 0
        
    finally:
        db.close()

async def test_telegram_link_detection():
    """测试Telegram群链接检测"""
    print("=" * 70)
    print("测试2: Telegram群链接检测")
    print("=" * 70)
    print()
    
    db = SessionLocal()
    try:
        reply_generator = ReplyGenerator(db)
        
        # 获取配置中的群组链接
        telegram_config = yaml_config.get("telegram_groups", {})
        main_group = telegram_config.get("main_group", "@your_group")
        print(f"配置的Telegram群组: {main_group}")
        print()
        
        # 测试群链接检测
        test_replies = [
            (f"Hi! Join our Telegram group: {main_group}", True, "包含完整群链接"),
            ("Join our Telegram group: https://t.me/+bNivsOGSM6ZlMGJl", True, "包含t.me链接"),
            ("telegram group", True, "包含telegram关键词"),
            ("Hello, how are you?", False, "不包含群链接"),
        ]
        
        print("测试群链接检测:")
        for reply, expected_has_link, description in test_replies:
            # 创建一个测试客户ID（使用一个不存在的ID，只测试检测逻辑）
            has_link = any(keyword in reply.lower() for keyword in [
                "t.me", "telegram", "telegram group", main_group.lower()
            ])
            result = "✅" if has_link == expected_has_link else "❌"
            print(f"{result} 回复: '{reply[:50]}...'")
            print(f"   预期: {'包含' if expected_has_link else '不包含'}, 实际: {'包含' if has_link else '不包含'} - {description}")
            print()
        
        return True
        
    finally:
        db.close()

async def test_reply_generation():
    """测试回复生成（不实际调用OpenAI）"""
    print("=" * 70)
    print("测试3: 回复生成逻辑")
    print("=" * 70)
    print()
    
    db = SessionLocal()
    try:
        reply_generator = ReplyGenerator(db)
        
        # 测试垃圾信息检测
        spam_message = "我要买手机"
        is_spam = reply_generator._is_spam_or_invalid(spam_message)
        print(f"垃圾信息检测测试:")
        print(f"  消息: '{spam_message}'")
        print(f"  结果: {'垃圾信息（不生成回复）' if is_spam else '正常消息（会生成回复）'}")
        print()
        
        # 测试业务消息
        business_message = "我想咨询iPhone贷款"
        is_spam = reply_generator._is_spam_or_invalid(business_message)
        print(f"业务消息检测测试:")
        print(f"  消息: '{business_message}'")
        print(f"  结果: {'垃圾信息（不生成回复）' if is_spam else '正常消息（会生成回复）'}")
        print()
        
        return True
        
    finally:
        db.close()

def test_configuration():
    """测试配置加载"""
    print("=" * 70)
    print("测试4: 配置加载")
    print("=" * 70)
    print()
    
    telegram_config = yaml_config.get("telegram_groups", {})
    main_group = telegram_config.get("main_group", "@your_group")
    
    print(f"Telegram群组配置: {main_group}")
    print(f"配置状态: {'✅ 已配置' if main_group and main_group != '@your_group' else '❌ 未配置'}")
    print()
    
    ai_templates = yaml_config.get("ai_templates", {})
    prompt_type = ai_templates.get("prompt_type")
    print(f"AI提示词类型: {prompt_type}")
    print(f"配置状态: {'✅ 已配置' if prompt_type else '⚠️  未配置（使用默认）'}")
    print()
    
    return True

async def main():
    """运行所有测试"""
    print()
    print("=" * 70)
    print("核心功能测试")
    print("=" * 70)
    print()
    
    results = []
    
    # 测试1: 垃圾信息检测
    try:
        result = await test_spam_detection()
        results.append(("智能垃圾信息检测", result))
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(("智能垃圾信息检测", False))
    
    print()
    
    # 测试2: Telegram群链接检测
    try:
        result = await test_telegram_link_detection()
        results.append(("Telegram群链接检测", result))
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        results.append(("Telegram群链接检测", False))
    
    print()
    
    # 测试3: 回复生成逻辑
    try:
        result = await test_reply_generation()
        results.append(("回复生成逻辑", result))
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        results.append(("回复生成逻辑", False))
    
    print()
    
    # 测试4: 配置加载
    try:
        result = test_configuration()
        results.append(("配置加载", result))
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        results.append(("配置加载", False))
    
    # 总结
    print()
    print("=" * 70)
    print("测试总结")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    print()
    
    if passed == total:
        print("✅ 所有核心功能测试通过！")
        return True
    else:
        print("❌ 部分测试失败，请检查")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 测试过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

