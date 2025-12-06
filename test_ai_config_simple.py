"""简单AI配置测试 - 不依赖完整配置"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_prompt_file():
    """测试提示词文件"""
    print("=" * 60)
    print("测试1: 提示词文件检查")
    print("=" * 60)
    
    prompt_file = "src/ai/prompts/iphone_loan_telegram.py"
    
    if os.path.exists(prompt_file):
        print(f"✅ 提示词文件存在: {prompt_file}")
        
        with open(prompt_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查关键内容
        checks = {
            "群组链接": "https://t.me/+Yz6RzEdD7JZjOGU1" in content,
            "iPhone": "iPhone" in content,
            "Loan Amount": "3,000" in content or "15,000" in content,
            "TRAFFIC GUIDANCE": "TRAFFIC GUIDANCE" in content or "traffic guidance" in content.lower(),
            "Auto-Recognition": "AUTO-RECOGNITION" in content or "auto-recognition" in content.lower(),
            "占位符已移除": "@your_group" not in content and "@your_channel" not in content,
        }
        
        print("\n内容检查:")
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
        
        # 显示群组链接出现次数
        link_count = content.count("https://t.me/+Yz6RzEdD7JZjOGU1")
        print(f"\n群组链接出现次数: {link_count}")
        
        if link_count > 0:
            print("✅ 群组链接已正确配置")
        else:
            print("❌ 未找到群组链接")
        
        return all(checks.values())
    else:
        print(f"❌ 提示词文件不存在: {prompt_file}")
        return False


def test_config_yaml():
    """测试config.yaml配置"""
    print("\n" + "=" * 60)
    print("测试2: config.yaml 配置检查")
    print("=" * 60)
    
    config_file = "config.yaml"
    
    if os.path.exists(config_file):
        print(f"✅ 配置文件存在: {config_file}")
        
        import yaml
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        
        # 检查AI模板配置
        ai_templates = config.get("ai_templates", {})
        prompt_type = ai_templates.get("prompt_type")
        
        print(f"\nAI模板配置:")
        print(f"  提示词类型: {prompt_type or '未设置'}")
        
        if prompt_type == "iphone_loan_telegram":
            print("  ✅ iPhone Loan Telegram 提示词已启用")
        else:
            print("  ⚠️  提示词类型未设置为 'iphone_loan_telegram'")
        
        # 检查Telegram群组配置
        telegram_groups = config.get("telegram_groups", {})
        if telegram_groups:
            main_group = telegram_groups.get("main_group")
            print(f"\nTelegram群组配置:")
            print(f"  主群组: {main_group or '未配置'}")
            
            if main_group and "t.me/+Yz6RzEdD7JZjOGU1" in main_group:
                print("  ✅ 群组链接已正确配置")
            elif main_group:
                print(f"  ⚠️  群组链接: {main_group}")
            else:
                print("  ⚠️  主群组未配置")
        else:
            print("\n⚠️  未找到 telegram_groups 配置")
        
        return prompt_type == "iphone_loan_telegram"
    else:
        print(f"❌ 配置文件不存在: {config_file}")
        return False


def test_prompt_import():
    """测试提示词导入"""
    print("\n" + "=" * 60)
    print("测试3: 提示词模块导入")
    print("=" * 60)
    
    try:
        from src.ai.prompts.iphone_loan_telegram import IPHONE_LOAN_TELEGRAM_PROMPT
        
        print("✅ 提示词模块导入成功")
        print(f"提示词长度: {len(IPHONE_LOAN_TELEGRAM_PROMPT)} 字符")
        
        # 检查群组链接
        if "https://t.me/+Yz6RzEdD7JZjOGU1" in IPHONE_LOAN_TELEGRAM_PROMPT:
            link_count = IPHONE_LOAN_TELEGRAM_PROMPT.count("https://t.me/+Yz6RzEdD7JZjOGU1")
            print(f"✅ 群组链接在提示词中出现 {link_count} 次")
        else:
            print("❌ 提示词中未找到群组链接")
        
        # 检查占位符
        if "@your_group" in IPHONE_LOAN_TELEGRAM_PROMPT or "@your_channel" in IPHONE_LOAN_TELEGRAM_PROMPT:
            print("⚠️  提示词中仍包含占位符")
        else:
            print("✅ 所有占位符已替换")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_prompt_template_class():
    """测试提示词模板类（不加载完整配置）"""
    print("\n" + "=" * 60)
    print("测试4: 提示词模板类（简化测试）")
    print("=" * 60)
    
    try:
        # 直接测试提示词文件
        from src.ai.prompts.iphone_loan_telegram import IPHONE_LOAN_TELEGRAM_PROMPT
        
        # 模拟配置
        test_config = {
            "telegram_groups": {
                "main_group": "https://t.me/+Yz6RzEdD7JZjOGU1",
                "main_channel": "https://t.me/+Yz6RzEdD7JZjOGU1"
            }
        }
        
        # 测试替换逻辑
        prompt = IPHONE_LOAN_TELEGRAM_PROMPT
        main_group = test_config["telegram_groups"].get("main_group", "@your_group")
        main_channel = test_config["telegram_groups"].get("main_channel", "@your_channel")
        
        prompt = prompt.replace("@your_group", main_group)
        prompt = prompt.replace("@your_channel", main_channel)
        
        if "https://t.me/+Yz6RzEdD7JZjOGU1" in prompt:
            print("✅ 提示词替换逻辑正常")
            print(f"   群组链接已正确替换")
        else:
            print("⚠️  提示词替换可能有问题")
        
        # 检查关键场景
        scenarios = {
            "第一条消息包含群组链接": "To speed up the review process" in prompt and "t.me" in prompt,
            "包含iPhone型号识别": "iPhone 12 Pro" in prompt or "Model" in prompt,
            "包含金额识别": "8,000" in prompt or "Amount" in prompt,
            "包含自动推进逻辑": "Auto Advance" in prompt or "auto-advance" in prompt.lower(),
        }
        
        print("\n关键场景检查:")
        for scenario, found in scenarios.items():
            status = "✅" if found else "⚠️"
            print(f"  {status} {scenario}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("AI配置测试（简化版）")
    print("=" * 60)
    print("\n开始测试...\n")
    
    results = []
    
    # 测试1: 提示词文件
    results.append(("提示词文件", test_prompt_file()))
    
    # 测试2: config.yaml
    results.append(("配置文件", test_config_yaml()))
    
    # 测试3: 提示词导入
    results.append(("提示词导入", test_prompt_import()))
    
    # 测试4: 提示词模板类
    results.append(("提示词模板", test_prompt_template_class()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 所有测试通过！AI配置正确。")
    else:
        print("\n⚠️  部分测试未通过，请检查配置。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

