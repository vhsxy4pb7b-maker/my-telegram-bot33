#!/bin/bash
# 回滚脚本

set -e

echo "🔄 开始回滚..."

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 请指定回滚版本"
    echo "用法: ./rollback.sh <version>"
    exit 1
fi

VERSION=$1

echo "📦 回滚到版本: $VERSION"

# 数据库回滚
if command -v alembic &> /dev/null; then
    echo "🗄️  回滚数据库..."
    alembic downgrade $VERSION || {
        echo "⚠️  数据库回滚失败，请手动检查"
    }
fi

# Git回滚（如果使用Git）
if [ -d ".git" ]; then
    echo "📝 回滚代码..."
    git checkout $VERSION || {
        echo "⚠️  代码回滚失败，请手动检查"
    }
fi

echo "✅ 回滚完成"
echo ""
echo "请检查系统状态:"
echo "  - 检查服务是否正常运行"
echo "  - 检查数据库状态"
echo "  - 查看日志文件"

