#!/bin/bash
# 部署验证脚本

set -e

echo "=========================================="
echo "部署验证 - 系统1.0版本"
echo "=========================================="
echo ""

PASS_COUNT=0
FAIL_COUNT=0

test_check() {
    local name=$1
    local command=$2
    
    echo -n "检查: $name ... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo "✓ 通过"
        ((PASS_COUNT++))
        return 0
    else
        echo "✗ 失败"
        ((FAIL_COUNT++))
        return 1
    fi
}

# 1. 检查配置文件
echo "1. 配置文件检查"
echo "----------------------------------------"
test_check ".env文件存在" "test -f .env"
test_check "config/config.yaml存在" "test -f config/config.yaml"

# 2. 检查必需的环境变量
echo ""
echo "2. 环境变量检查"
echo "----------------------------------------"
if [ -f .env ]; then
    test_check "DATABASE_URL配置" "grep -q 'DATABASE_URL=' .env && ! grep -q 'your_' .env | grep DATABASE_URL"
    test_check "FACEBOOK配置" "grep -q 'FACEBOOK_ACCESS_TOKEN=' .env && ! grep -q 'your_facebook' .env | grep FACEBOOK_ACCESS_TOKEN"
    test_check "OPENAI配置" "grep -q 'OPENAI_API_KEY=' .env && ! grep -q 'your_openai' .env | grep OPENAI_API_KEY"
    test_check "TELEGRAM配置" "grep -q 'TELEGRAM_BOT_TOKEN=' .env && ! grep -q 'your_telegram' .env | grep TELEGRAM_BOT_TOKEN"
fi

# 3. 检查数据库连接
echo ""
echo "3. 数据库连接检查"
echo "----------------------------------------"
test_check "数据库连接" "python3 -c 'from src.database.database import engine; engine.connect()'"

# 4. 检查数据库迁移
echo ""
echo "4. 数据库迁移检查"
echo "----------------------------------------"
if command -v alembic &> /dev/null; then
    test_check "Alembic配置" "test -f alembic.ini"
    test_check "迁移脚本存在" "test -d alembic/versions && [ \"\$(ls -A alembic/versions)\" ]"
else
    echo "检查: Alembic未安装 ... ⊘ 跳过"
fi

# 5. 检查应用启动
echo ""
echo "5. 应用启动检查"
echo "----------------------------------------"
test_check "FastAPI应用创建" "python3 -c 'from src.main import app; assert app is not None'"

# 6. 检查关键端点
echo ""
echo "6. API端点检查"
echo "----------------------------------------"
test_check "健康检查端点" "python3 -c 'from src.main import app; routes = [r.path for r in app.routes]; assert \"/health\" in routes or any(\"/health\" in r for r in routes)'"

# 7. 检查日志目录
echo ""
echo "7. 日志目录检查"
echo "----------------------------------------"
test_check "logs目录存在" "test -d logs || mkdir -p logs"

# 总结
echo ""
echo "=========================================="
echo "验证总结"
echo "=========================================="
echo "通过: $PASS_COUNT"
echo "失败: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✓ 部署验证通过！系统可以部署。"
    exit 0
else
    echo "✗ 发现 $FAIL_COUNT 个问题，请修复后再部署。"
    exit 1
fi

