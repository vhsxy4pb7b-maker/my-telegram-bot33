"""从重定向 URL 中提取访问令牌"""
import urllib.parse
import sys
from typing import Optional, Dict, Any


def extract_token_from_url(url: str) -> Optional[Dict[str, Any]]:
    """从重定向 URL 中提取 access_token
    
    Args:
        url: 包含访问令牌的重定向URL
        
    Returns:
        包含访问令牌信息的字典，如果提取失败则返回None
    """
    if not url or not isinstance(url, str):
        print("✗ URL 无效")
        return None
        
    try:
        # 分离 fragment（# 后面的部分）
        if '#' in url:
            fragment = url.split('#', 1)[1]
            params = urllib.parse.parse_qs(fragment)
        else:
            # 尝试从查询参数中提取
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)

        if 'access_token' not in params or not params['access_token']:
            return None

        access_token = params['access_token'][0]
        expires_in = params.get('expires_in', ['N/A'])[0]
        token_type = params.get('token_type', ['bearer'])[0]

        return {
            'access_token': access_token,
            'expires_in': expires_in,
            'token_type': token_type
        }
    except (ValueError, KeyError, IndexError) as e:
        print(f"✗ 解析 URL 失败: {e}")
        return None
    except Exception as e:
        print(f"✗ 发生未知错误: {e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("Facebook 访问令牌提取工具")
    print("=" * 60)

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("\n请粘贴授权后的重定向 URL：")
        print("格式: http://localhost:8000/oauth/callback#access_token=TOKEN&...")
        url = input("\nURL: ").strip()

    if not url:
        print("✗ URL 不能为空")
        sys.exit(1)

    # 提取令牌
    token_info = extract_token_from_url(url)

    if token_info:
        print("\n" + "=" * 60)
        print("✓ 访问令牌提取成功！")
        print("=" * 60)
        print(f"\n访问令牌: {token_info['access_token']}")
        print(f"令牌类型: {token_info['token_type']}")
        print(f"过期时间: {token_info['expires_in']} 秒")

        # 计算过期天数
        expires_in = token_info['expires_in']
        if isinstance(expires_in, str) and expires_in.isdigit():
            days = int(expires_in) // 86400
            hours = (int(expires_in) % 86400) // 3600
            if days > 0:
                print(f"          (约 {days} 天 {hours} 小时)")
            else:
                print(f"          (约 {hours} 小时)")
        elif isinstance(expires_in, int):
            days = expires_in // 86400
            hours = (expires_in % 86400) // 3600
            if days > 0:
                print(f"          (约 {days} 天 {hours} 小时)")
            else:
                print(f"          (约 {hours} 小时)")

        print("\n" + "=" * 60)
        print("下一步")
        print("=" * 60)
        print("\n请将以下内容添加到 .env 文件：")
        print(f"FACEBOOK_ACCESS_TOKEN={token_info['access_token']}")

        # 询问是否自动更新
        update = input("\n是否自动更新到 .env 文件? (y/N): ").strip().lower()
        if update == 'y':
            try:
                from configure_api_keys import update_env_file
                if update_env_file("FACEBOOK_ACCESS_TOKEN", token_info['access_token']):
                    print("✓ 已更新到 .env 文件")
                else:
                    print("⚠️  更新 .env 文件失败，请手动更新")
            except ImportError:
                print("⚠️  无法导入配置模块，请手动更新 .env 文件")
            except Exception as e:
                print(f"⚠️  更新 .env 文件时出错: {e}")
                print("请手动将以下内容添加到 .env 文件：")
                print(f"FACEBOOK_ACCESS_TOKEN={token_info['access_token']}")

        print("\n提示：这是短期令牌（1-2小时）")
        print("要获取长期令牌（60天），运行: python exchange_token.py")

    else:
        print("\n✗ 无法从 URL 中提取访问令牌")
        print("\n请确保 URL 格式正确：")
        print("http://localhost:8000/oauth/callback#access_token=TOKEN&token_type=bearer&expires_in=5183944")


if __name__ == "__main__":
    main()
