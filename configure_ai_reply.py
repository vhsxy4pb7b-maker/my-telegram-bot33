"""AI 回复规则配置工具"""
import yaml
import os
import shutil

def load_config():
    """加载配置文件"""
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_config(config):
    """保存配置文件"""
    config_file = "config.yaml"
    # 备份原文件
    if os.path.exists(config_file):
        shutil.copy(config_file, f"{config_file}.backup")
    
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return True

def configure_ai_templates():
    """配置 AI 回复模板"""
    print("=" * 60)
    print("配置 AI 回复模板")
    print("=" * 60)
    
    config = load_config()
    
    if "ai_templates" not in config:
        config["ai_templates"] = {}
    
    templates = config["ai_templates"]
    
    print("\n当前配置的模板：")
    print(f"  问候语: {templates.get('greeting', '未设置')}")
    print(f"  收集信息: {templates.get('collecting_info', '未设置')}")
    print(f"  处理中: {templates.get('processing', '未设置')}")
    print(f"  默认回复: {templates.get('fallback', '未设置')}")
    
    print("\n" + "=" * 60)
    print("请选择要配置的模板（留空跳过）：")
    print("=" * 60)
    
    # 问候语
    greeting = input("\n1. 问候语（客户首次联系时）[留空跳过]: ").strip()
    if greeting:
        templates["greeting"] = greeting
        print("✓ 问候语已更新")
    
    # 收集信息
    collecting_info = input("\n2. 收集信息提示 [留空跳过]: ").strip()
    if collecting_info:
        templates["collecting_info"] = collecting_info
        print("✓ 收集信息提示已更新")
    
    # 处理中
    processing = input("\n3. 处理中提示 [留空跳过]: ").strip()
    if processing:
        templates["processing"] = processing
        print("✓ 处理中提示已更新")
    
    # 默认回复
    fallback = input("\n4. 默认回复（无法理解时）[留空跳过]: ").strip()
    if fallback:
        templates["fallback"] = fallback
        print("✓ 默认回复已更新")
    
    config["ai_templates"] = templates
    return config

def configure_system_prompt():
    """配置系统提示词"""
    print("\n" + "=" * 60)
    print("配置系统提示词（AI 的角色和行为）")
    print("=" * 60)
    
    print("\n系统提示词定义了 AI 的角色、职责和回复风格。")
    print("当前提示词在: src/ai/prompt_templates.py")
    print("\n示例提示词：")
    print("-" * 60)
    print("""你是一个专业的AI智能客服助手。你的职责是：
1. 友好、专业地回复客户咨询
2. 收集客户的基本信息（姓名、联系方式、需求等）
3. 理解客户意图，提供初步帮助
4. 如果无法解决，引导客户提供更多信息以便人工处理

请用中文回复，保持礼貌和专业。""")
    print("-" * 60)
    
    print("\n要修改系统提示词，请编辑文件:")
    print("  src/ai/prompt_templates.py")
    print("  修改 build_system_prompt() 方法")
    print("\n详细说明请查看: CONFIGURE_AI_REPLY.md")

def main():
    """主函数"""
    print("=" * 60)
    print("AI 回复规则配置工具")
    print("=" * 60)
    print("\n本工具将帮助您配置 AI 的回复模板")
    print("系统提示词需要手动编辑代码文件")
    
    try:
        # 配置模板
        config = configure_ai_templates()
        
        # 保存配置
        if config:
            if save_config(config):
                print("\n" + "=" * 60)
                print("✅ 配置已保存！")
                print("=" * 60)
                print("\n配置文件: config.yaml")
                print("备份文件: config.yaml.backup")
                print("\n⚠️  需要重启服务使配置生效:")
                print("  1. 停止当前服务（Ctrl+C）")
                print("  2. 重新启动: python run.py")
            else:
                print("\n✗ 保存配置失败")
        
        # 系统提示词说明
        configure_system_prompt()
        
        print("\n" + "=" * 60)
        print("配置完成")
        print("=" * 60)
        print("\n📚 详细说明请查看: CONFIGURE_AI_REPLY.md")
        
    except KeyboardInterrupt:
        print("\n\n已取消操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")

if __name__ == "__main__":
    main()

