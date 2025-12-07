"""配置页面自动回复工具"""
import sys
import os
from src.config.page_settings import PageSettings
import yaml


def list_pages(settings: PageSettings):
    """列出所有已配置的页面"""
    pages = settings.get_all_pages()
    
    if not pages:
        print("\n暂无已配置的页面")
        return
    
    print("\n已配置的页面:")
    print("=" * 60)
    for page_id in pages:
        config = settings.get_page_config(page_id)
        enabled = "✅ 启用" if config.get("auto_reply_enabled", True) else "❌ 禁用"
        print(f"页面ID: {page_id}")
        print(f"  自动回复: {enabled}")
        if "name" in config:
            print(f"  页面名称: {config['name']}")
        print()


def add_page(settings: PageSettings):
    """添加或更新页面配置"""
    print("\n" + "=" * 60)
    print("配置页面自动回复")
    print("=" * 60)
    
    page_id = input("\n请输入页面ID: ").strip()
    if not page_id:
        print("❌ 页面ID不能为空")
        return
    
    # 检查是否已存在
    existing_config = settings.get_page_config(page_id)
    if existing_config:
        current_status = "启用" if existing_config.get("auto_reply_enabled", True) else "禁用"
        print(f"\n页面 {page_id} 已存在，当前状态: {current_status}")
        update = input("是否更新? (y/N): ").strip().lower()
        if update != 'y':
            return
    
    # 获取页面名称（可选）
    page_name = input("页面名称（可选，留空跳过）: ").strip()
    
    # 询问是否启用自动回复
    enable_input = input("是否启用自动回复? (Y/n): ").strip().lower()
    auto_reply_enabled = enable_input != 'n'
    
    # 准备配置
    config = {"auto_reply_enabled": auto_reply_enabled}
    if page_name:
        config["name"] = page_name
    
    # 保存配置
    if settings.add_page(page_id, **config):
        status = "✅ 已启用" if auto_reply_enabled else "❌ 已禁用"
        print(f"\n{status} 页面 {page_id} 的自动回复配置")
        if page_name:
            print(f"页面名称: {page_name}")
    else:
        print("\n❌ 保存配置失败")


def remove_page(settings: PageSettings):
    """移除页面配置"""
    print("\n" + "=" * 60)
    print("移除页面配置")
    print("=" * 60)
    
    pages = settings.get_all_pages()
    if not pages:
        print("\n暂无已配置的页面")
        return
    
    print("\n已配置的页面:")
    for i, page_id in enumerate(pages, 1):
        config = settings.get_page_config(page_id)
        name = config.get("name", "未命名")
        print(f"{i}. {page_id} ({name})")
    
    page_id = input("\n请输入要移除的页面ID: ").strip()
    if not page_id:
        print("❌ 页面ID不能为空")
        return
    
    if page_id not in pages:
        print(f"❌ 页面 {page_id} 不存在")
        return
    
    confirm = input(f"确认移除页面 {page_id} 的配置? (y/N): ").strip().lower()
    if confirm == 'y':
        if settings.remove_page(page_id):
            print(f"✅ 已移除页面 {page_id} 的配置")
        else:
            print("❌ 移除失败")
    else:
        print("已取消")


def check_page_status(settings: PageSettings):
    """检查页面自动回复状态"""
    print("\n" + "=" * 60)
    print("检查页面自动回复状态")
    print("=" * 60)
    
    page_id = input("\n请输入页面ID（留空检查全局设置）: ").strip()
    
    if page_id:
        enabled = settings.is_auto_reply_enabled(page_id)
        config = settings.get_page_config(page_id)
        
        print(f"\n页面ID: {page_id}")
        if config:
            status = "✅ 启用" if enabled else "❌ 禁用"
            print(f"自动回复: {status}")
            if "name" in config:
                print(f"页面名称: {config['name']}")
        else:
            print("该页面未单独配置，使用全局设置")
            global_enabled = settings.is_auto_reply_enabled()
            status = "✅ 启用" if global_enabled else "❌ 禁用"
            print(f"全局自动回复: {status}")
    else:
        # 检查全局设置
        enabled = settings.is_auto_reply_enabled()
        status = "✅ 启用" if enabled else "❌ 禁用"
        print(f"\n全局自动回复: {status}")
        
        # 显示所有页面配置
        pages = settings.get_all_pages()
        if pages:
            print(f"\n已配置的页面数量: {len(pages)}")
            for page_id in pages:
                page_enabled = settings.is_auto_reply_enabled(page_id)
                page_status = "✅ 启用" if page_enabled else "❌ 禁用"
                config = settings.get_page_config(page_id)
                name = config.get("name", "未命名")
                print(f"  - {page_id} ({name}): {page_status}")


def main():
    """主函数"""
    settings = PageSettings()
    
    print("=" * 60)
    print("页面自动回复配置工具")
    print("=" * 60)
    print("\n请选择操作:")
    print("1. 列出所有已配置的页面")
    print("2. 添加/更新页面配置")
    print("3. 移除页面配置")
    print("4. 检查页面自动回复状态")
    print("5. 退出")
    
    while True:
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            list_pages(settings)
        elif choice == "2":
            add_page(settings)
        elif choice == "3":
            remove_page(settings)
        elif choice == "4":
            check_page_status(settings)
        elif choice == "5":
            print("\n再见！")
            break
        else:
            print("❌ 无效选择，请输入 1-5")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)


