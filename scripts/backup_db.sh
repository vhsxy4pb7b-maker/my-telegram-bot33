#!/bin/bash
# 数据库备份脚本
# 使用方法: ./backup_db.sh

# 配置
BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7  # 保留最近7天的备份

# 从环境变量读取数据库URL
if [ -z "$DATABASE_URL" ]; then
    echo "错误: DATABASE_URL 环境变量未设置"
    exit 1
fi

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 判断数据库类型
if [[ "$DATABASE_URL" == postgresql* ]] || [[ "$DATABASE_URL" == postgres* ]]; then
    # PostgreSQL备份
    BACKUP_FILE="$BACKUP_DIR/postgres_backup_$DATE.sql"
    echo "开始备份PostgreSQL数据库..."
    
    # 使用pg_dump备份
    pg_dump "$DATABASE_URL" > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        # 压缩备份文件
        gzip "$BACKUP_FILE"
        echo "备份成功: ${BACKUP_FILE}.gz"
        
        # 删除旧备份（保留最近N天）
        find "$BACKUP_DIR" -name "postgres_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
        echo "已清理 $RETENTION_DAYS 天前的备份文件"
    else
        echo "备份失败"
        exit 1
    fi
    
elif [[ "$DATABASE_URL" == sqlite* ]]; then
    # SQLite备份
    BACKUP_FILE="$BACKUP_DIR/sqlite_backup_$DATE.db"
    echo "开始备份SQLite数据库..."
    
    # 提取SQLite文件路径
    DB_PATH=$(echo "$DATABASE_URL" | sed 's/sqlite:\/\/\///')
    
    if [ -f "$DB_PATH" ]; then
        cp "$DB_PATH" "$BACKUP_FILE"
        
        if [ $? -eq 0 ]; then
            # 压缩备份文件
            gzip "$BACKUP_FILE"
            echo "备份成功: ${BACKUP_FILE}.gz"
            
            # 删除旧备份
            find "$BACKUP_DIR" -name "sqlite_backup_*.db.gz" -mtime +$RETENTION_DAYS -delete
            echo "已清理 $RETENTION_DAYS 天前的备份文件"
        else
            echo "备份失败"
            exit 1
        fi
    else
        echo "错误: 数据库文件不存在: $DB_PATH"
        exit 1
    fi
else
    echo "错误: 不支持的数据库类型"
    exit 1
fi

echo "备份完成"
