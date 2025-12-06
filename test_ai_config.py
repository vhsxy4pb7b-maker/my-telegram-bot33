"""测试AI配置 - 验证iPhone Loan Telegram提示词配置"""
import asyncio
import sys
import os
from sqlalchemy.orm import Session

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ai.prompt_templates import PromptTemplates
from src.ai.reply_generator import ReplyGenerator
from src.database.database import SessionLocal
from src.config import yaml_config


def test_prompt_loading():
    """测试提示词加载"""
    print("=" * 60)
    print("测试1: 提示词加载")
    print("=" * 60)
    
    templates = PromptTemplates()
    prompt_type = templates.templates.get("prompt_type")
    
    print(f"配置的提示词类型: {prompt_type}")
    
    if prompt_type == "iphone_loan_telegram":
        print("✅ iPhone Loan Telegram 提示词已启用")
    else:
        print(f"⚠️  当前提示词类型: {prompt_type or '默认'}")
    
    # 构建系统提示词
    system_prompt = templates.build_system_prompt(prompt_type=prompt_type)
    
    print(f"\n提示词长度: {len(system_prompt)} 字符")
    print(f"提示词前200字符预览:")
    print("-" * 60)
    print(system_prompt[:200] + "...")
    print("-" * 60)
    
    # 检查群组链接
    if "https://t.me/+Yz6RzEdD7JZjOGU1" in system_prompt:
        print("\n✅ 群组链接已正确配置")
    elif "@your_group" in system_prompt:
        print("\n⚠️  提示词中仍包含占位符 @your_group")
    else:
        print("\n⚠️  未找到群组链接")
    
    return system_prompt


def test_telegram_groups_config():
    """测试Telegram群组配置"""
    print("\n" + "=" * 60)
    print("测试2: Telegram群组配置")
    print("=" * 60)
    
    telegram_config = yaml_config.get("telegram_groups", {})
    
    if telegram_config:
        main_group = telegram_config.get("main_group")
        main_channel = telegram_config.get("main_channel")
        
        print(f"主群组: {main_group or '未配置'}")
        print(f"主频道: {main_channel or '未配置'}")
        
        if main_group and "t.me" in main_group:
            print("✅ 群组链接格式正确")
        elif main_group:
            print(f"⚠️  群组配置: {main_group}")
        else:
            print("⚠️  未配置主群组")
    else:
        print("⚠️  未找到 telegram_groups 配置")


def test_ai_reply_structure():
    """测试AI回复结构（不实际调用API）"""
    print("\n" + "=" * 60)
    print("测试3: AI回复结构")
    print("=" * 60)
    
    templates = PromptTemplates()
    prompt_type = templates.templates.get("prompt_type")
    
    # 检查提示词是否包含关键元素
    system_prompt = templates.build_system_prompt(prompt_type=prompt_type)
    
    key_elements = {
        "TRAFFIC GUIDANCE": "TRAFFIC GUIDANCE" in system_prompt or "traffic guidance" in system_prompt.lower(),
        "iPhone": "iPhone" in system_prompt,
        "Loan Amount": "Loan Amount" in system_prompt or "3,000" in system_prompt,
        "Auto-Recognition": "AUTO-RECOGNITION" in system_prompt or "auto-recognition" in system_prompt.lower(),
        "Group Invitation": "join" in system_prompt.lower() and "group" in system_prompt.lower(),
    }
    
    print("关键元素检查:")
    for element, found in key_elements.items():
        status = "✅" if found else "❌"
        print(f"  {status} {element}")
    
    return all(key_elements.values())


async def test_ai_reply_generation():
    """测试AI回复生成（需要OpenAI API）"""
    print("\n" + "=" * 60)
    print("测试4: AI回复生成（需要OpenAI API）")
    print("=" * 60)
    
    try:
        from src.config import settings
        
        if not settings.openai_api_key or settings.openai_api_key.startswith("your_"):
            print("⚠️  OpenAI API密钥未配置或为占位符")
            print("   跳过实际API测试")
            return False
        
        db = SessionLocal()
        try:
            generator = ReplyGenerator(db)
            
            # 测试消息
            test_messages = [
                "Hello",
                "iPhone 13",
                "Want to borrow 8000",
                "iPhone 12 Pro, 10000"
            ]
            
            print("测试消息:")
            for i, msg in enumerate(test_messages, 1):
                print(f"\n{i}. 用户消息: {msg}")
                print("   生成回复中...")
                
                try:
                    # 创建一个临时客户用于测试
                    from src.database.models import Customer, Platform
                    test_customer = Customer(
                        platform=Platform.FACEBOOK,
                        platform_user_id="test_user_123",
                        name="Test User"
                    )
                    db.add(test_customer)
                    db.commit()
                    db.refresh(test_customer)
                    
                    reply = await generator.generate_reply(
                        customer_id=test_customer.id,
                        message_content=msg,
                        customer_name="Test User"
                    )
                    
                    print(f"   AI回复: {reply[:150]}...")
                    
                    # 检查回复是否包含群组链接
                    if "t.me/+Yz6RzEdD7JZjOGU1" in reply:
                        print("   ✅ 回复包含群组链接")
                    elif "t.me" in reply:
                        print("   ⚠️  回复包含Telegram链接（可能不是目标群组）")
                    else:
                        print("   ⚠️  回复未包含群组链接")
                    
                    # 清理测试数据
                    db.delete(test_customer)
                    db.commit()
                    
                except Exception as e:
                    print(f"   ❌ 生成回复失败: {str(e)}")
            
            return True
            
        finally:
            db.close()
            
    except ImportError:
        print("⚠️  无法导入配置模块")
        return False
    except Exception as e:
        print(f"⚠️  测试失败: {str(e)}")
        return False


def test_config_file():
    """测试配置文件"""
    print("\n" + "=" * 60)
    print("测试5: 配置文件检查")
    print("=" * 60)
    
    config_path = "config.yaml"
    if os.path.exists(config_path):
        print(f"✅ 配置文件存在: {config_path}")
        
        # 检查关键配置
        ai_templates = yaml_config.get("ai_templates", {})
        prompt_type = ai_templates.get("prompt_type")
        
        print(f"   提示词类型: {prompt_type or '未设置'}")
        
        telegram_groups = yaml_config.get("telegram_groups", {})
        if telegram_groups:
            print(f"   Telegram群组: {telegram_groups.get('main_group', '未配置')}")
        else:
            print("   ⚠️  未配置 telegram_groups")
    else:
        print(f"❌ 配置文件不存在: {config_path}")


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("AI配置测试")
    print("=" * 60)
    print("\n开始测试AI配置...\n")
    
    # 测试1: 提示词加载
    system_prompt = test_prompt_loading()
    
    # 测试2: Telegram群组配置
    test_telegram_groups_config()
    
    # 测试3: AI回复结构
    structure_ok = test_ai_reply_structure()
    
    # 测试4: AI回复生成（可选，需要API）
    print("\n跳过API测试（避免消耗API配额）")
    print("如需测试实际AI回复，请取消注释下面的代码")
    # await test_ai_reply_generation()
    
    # 测试5: 配置文件
    test_config_file()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if structure_ok:
        print("✅ 提示词结构检查通过")
    else:
        print("⚠️  提示词结构可能不完整")
    
    if "https://t.me/+Yz6RzEdD7JZjOGU1" in system_prompt:
        print("✅ 群组链接已正确配置")
    else:
        print("⚠️  群组链接可能未正确配置")
    
    print("\n测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

