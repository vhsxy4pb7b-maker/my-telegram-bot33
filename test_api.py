"""API 测试脚本 - 快速测试系统功能"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_root():
    """测试根路径"""
    print("=" * 60)
    print("测试 1: 系统信息 (GET /)")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("✓ 测试通过\n")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}\n")
        return False


def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("测试 2: 健康检查 (GET /health)")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("✓ 测试通过\n")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}\n")
        return False


def test_webhook_verify():
    """测试 Facebook Webhook 验证"""
    print("=" * 60)
    print("测试 3: Facebook Webhook 验证 (GET /webhook)")
    print("=" * 60)
    try:
        # 从 .env 读取验证令牌（简化版，实际应该从配置文件读取）
        verify_token = "your_webhook_verify_token"  # 替换为实际值

        params = {
            "hub.mode": "subscribe",
            "hub.verify_token": verify_token,
            "hub.challenge": "test_challenge_123"
        }

        response = requests.get(f"{BASE_URL}/webhook", params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")

        if response.status_code == 200 and "test_challenge_123" in response.text:
            print("✓ Webhook 验证测试通过\n")
            return True
        else:
            print("⚠️  Webhook 验证可能需要配置正确的验证令牌\n")
            return False
    except Exception as e:
        print(f"✗ 测试失败: {e}\n")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Facebook 客服自动化系统 - API 测试")
    print("=" * 60)
    print(f"\n测试服务器: {BASE_URL}")
    print("确保服务正在运行 (python run.py)\n")

    results = []

    # 运行测试
    results.append(("系统信息", test_root()))
    results.append(("健康检查", test_health()))
    results.append(("Webhook 验证", test_webhook_verify()))

    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
    else:
        print("\n⚠️  部分测试失败，请检查服务状态和配置。")

    print("\n" + "=" * 60)
    print("更多信息:")
    print("- API 文档: http://localhost:8000/docs")
    print("- 使用指南: 查看 USAGE_GUIDE.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
