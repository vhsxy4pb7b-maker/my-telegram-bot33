"""快速授权工具 - 简化权限配置流程"""
import sys
import os
import webbrowser
import urllib.parse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook权限快速授权工具")
    print("=" * 60)
    
    # 获取App ID
    try:
        from src.config import settings
        app_id = settings.facebook_app_id
        print(f"\n✅ 使用App ID: {app_id}")
    except Exception as e:
        print(f"⚠️  无法读取配置: {str(e)}")
        app_id = input("请输入Facebook App ID: ").strip()
        if not app_id:
            print("❌ App ID不能为空")
            return
    
    # 生成授权URL
    redirect_uri = "http://localhost:8000/oauth/callback"
    scope = "pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management"
    
    base_url = "https://www.facebook.com/v18.0/dialog/oauth"
    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "token"
    }
    
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{base_url}?{query_string}"
    
    print("\n" + "=" * 60)
    print("授权URL已生成")
    print("=" * 60)
    print(f"\n{auth_url}\n")
    print("=" * 60)
    
    print("\n包含的权限:")
    print("  ✅ pages_messaging - 发送和接收消息")
    print("  ✅ pages_read_engagement - 读取页面互动数据")
    print("  ✅ pages_manage_metadata - 管理页面元数据")
    print("  ✅ pages_manage_posts - 管理页面帖子")
    print("  ✅ ads_read - 读取广告数据")
    print("  ✅ ads_management - 管理广告")
    
    print("\n" + "=" * 60)
    print("下一步操作")
    print("=" * 60)
    
    # 询问是否打开浏览器
    if sys.stdin.isatty():
        print("\n是否在浏览器中打开授权URL？(y/n): ", end="")
        try:
            choice = input().strip().lower()
            if choice in ['y', 'yes', '']:
                print("\n正在打开浏览器...")
                webbrowser.open(auth_url)
                print("✅ 浏览器已打开")
            else:
                print("\n请手动复制上面的URL并在浏览器中打开")
        except:
            print("\n请手动复制上面的URL并在浏览器中打开")
    else:
        print("\n请手动复制上面的URL并在浏览器中打开")
    
    print("\n" + "=" * 60)
    print("授权后操作")
    print("=" * 60)
    print("\n授权成功后，浏览器会重定向到类似这样的URL：")
    print("http://localhost:8000/oauth/callback#access_token=TOKEN&...")
    print("\n请运行以下命令提取并更新令牌：")
    print("  python extract_token.py")
    print("\n然后运行以下命令验证权限：")
    print("  python check_facebook_permissions.py")


if __name__ == "__main__":
    main()




