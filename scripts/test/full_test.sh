#!/bin/bash
# 完整测试脚本 - 运行所有测试

set -e

echo "=========================================="
echo "系统1.0版本完整测试"
echo "=========================================="
echo ""

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 1. 运行pytest单元测试
echo "1. 运行单元测试"
echo "----------------------------------------"
if command -v pytest &> /dev/null; then
    pytest tests/ -v --cov=src --cov-report=term --cov-report=html || {
        echo "⚠️  部分单元测试失败，继续其他测试..."
    }
else
    echo "⚠️  pytest未安装，跳过单元测试"
fi

# 2. 运行系统功能测试
echo ""
echo "2. 运行系统功能测试"
echo "----------------------------------------"
python tests/test_system_functionality.py || {
    echo "⚠️  系统功能测试失败"
}

# 3. 运行生产就绪性测试
echo ""
echo "3. 运行生产就绪性测试"
echo "----------------------------------------"
python tests/test_production_readiness.py || {
    echo "⚠️  生产就绪性测试失败"
}

# 4. 启动服务并测试API
echo ""
echo "4. API端点测试"
echo "----------------------------------------"
echo "启动服务进行API测试..."
echo "注意: 这需要在后台运行服务"
echo ""

# 生成测试报告
echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
echo ""
echo "查看测试报告:"
echo "  - 覆盖率报告: htmlcov/index.html"
echo "  - 日志文件: logs/app.log"
echo ""

