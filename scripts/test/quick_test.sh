#!/bin/bash
# 快速测试脚本 - 验证系统1.0版本基本功能

set -e

echo "=========================================="
echo "系统1.0版本快速测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# 测试函数
test_check() {
    local name=$1
    local command=$2
    
    echo -n "测试: $name ... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((PASS_COUNT++))
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        ((FAIL_COUNT++))
        return 1
    fi
}

test_skip() {
    local name=$1
    echo -e "测试: $name ... ${YELLOW}⊘ 跳过${NC}"
    ((SKIP_COUNT++))
}

# 1. 检查Python版本
echo "1. 环境检查"
echo "----------------------------------------"
test_check "Python 3.9+" "python3 --version | grep -E 'Python 3\.(9|1[0-9])'"
test_check "pip已安装" "python3 -m pip --version"

# 2. 检查依赖
echo ""
echo "2. 依赖检查"
echo "----------------------------------------"
test_check "requirements.txt存在" "test -f requirements.txt"
if [ -f requirements.txt ]; then
    test_check "依赖已安装" "python3 -c 'import fastapi, sqlalchemy, openai'"
fi

# 3. 检查配置文件
echo ""
echo "3. 配置文件检查"
echo "----------------------------------------"
test_check ".env文件存在" "test -f .env"
test_check "config/config.yaml存在" "test -f config/config.yaml || test -f config/config.yaml.example"

# 4. 检查数据库
echo ""
echo "4. 数据库检查"
echo "----------------------------------------"
if python3 -c "from src.config import settings; import sys; sys.exit(0 if 'sqlite' in settings.database_url.lower() else 1)" 2>/dev/null; then
    test_skip "数据库连接（使用SQLite）"
else
    test_check "PostgreSQL可连接" "python3 -c 'from src.database.database import engine; engine.connect()'"
fi

# 5. 测试配置加载
echo ""
echo "5. 配置加载测试"
echo "----------------------------------------"
test_check "环境变量配置加载" "python3 -c 'from src.config import settings; assert hasattr(settings, \"database_url\")'"
test_check "YAML配置加载" "python3 -c 'from src.config.loader import load_yaml_config; load_yaml_config(\"config/config.yaml\")' 2>/dev/null || python3 -c 'from src.config.loader import load_yaml_config; load_yaml_config(\"config/config.yaml.example\")'"

# 6. 测试数据库模型
echo ""
echo "6. 数据库模型测试"
echo "----------------------------------------"
test_check "数据库模型导入" "python3 -c 'from src.database.models import Customer, Conversation, CollectedData, Review'"

# 7. 测试核心模块
echo ""
echo "7. 核心模块测试"
echo "----------------------------------------"
test_check "Facebook模块导入" "python3 -c 'from src.facebook.api_client import FacebookAPIClient'"
test_check "AI模块导入" "python3 -c 'from src.ai.reply_generator import ReplyGenerator'"
test_check "数据收集模块导入" "python3 -c 'from src.collector.data_collector import DataCollector'"
test_check "过滤引擎导入" "python3 -c 'from src.collector.filter_engine import FilterEngine'"
test_check "Telegram模块导入" "python3 -c 'from src.telegram.bot_handler import router'"

# 8. 测试应用启动
echo ""
echo "8. 应用启动测试"
echo "----------------------------------------"
test_check "FastAPI应用创建" "python3 -c 'from src.main import app; assert app is not None'"

# 9. 运行pytest测试（如果可用）
echo ""
echo "9. 单元测试"
echo "----------------------------------------"
if command -v pytest &> /dev/null; then
    if pytest tests/test_database_models.py -v --tb=short > /dev/null 2>&1; then
        echo -e "测试: 数据库模型单元测试 ... ${GREEN}✓ 通过${NC}"
        ((PASS_COUNT++))
    else
        echo -e "测试: 数据库模型单元测试 ... ${RED}✗ 失败${NC}"
        ((FAIL_COUNT++))
    fi
else
    test_skip "pytest未安装"
fi

# 总结
echo ""
echo "=========================================="
echo "测试总结"
echo "=========================================="
echo -e "${GREEN}通过: $PASS_COUNT${NC}"
echo -e "${RED}失败: $FAIL_COUNT${NC}"
echo -e "${YELLOW}跳过: $SKIP_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ 所有关键测试通过！系统基本功能正常。${NC}"
    exit 0
else
    echo -e "${RED}✗ 发现 $FAIL_COUNT 个失败项，请检查并修复。${NC}"
    exit 1
fi

