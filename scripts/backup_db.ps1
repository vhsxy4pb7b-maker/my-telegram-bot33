# 数据库备份脚本 (PowerShell版本)
# 使用方法: .\backup_db.ps1

# 配置
$BACKUP_DIR = "backups"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$RETENTION_DAYS = 7  # 保留最近7天的备份

# 从环境变量读取数据库URL
$DATABASE_URL = $env:DATABASE_URL
if (-not $DATABASE_URL) {
    Write-Host "错误: DATABASE_URL 环境变量未设置" -ForegroundColor Red
    exit 1
}

# 创建备份目录
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}

# 判断数据库类型
if ($DATABASE_URL -match "^postgresql" -or $DATABASE_URL -match "^postgres") {
    # PostgreSQL备份
    $BACKUP_FILE = "$BACKUP_DIR\postgres_backup_$DATE.sql"
    Write-Host "开始备份PostgreSQL数据库..."
    
    # 使用pg_dump备份（需要安装PostgreSQL客户端）
    try {
        pg_dump $DATABASE_URL | Out-File -FilePath $BACKUP_FILE -Encoding UTF8
        
        # 压缩备份文件（需要7-Zip或类似工具）
        if (Get-Command Compress-Archive -ErrorAction SilentlyContinue) {
            Compress-Archive -Path $BACKUP_FILE -DestinationPath "$BACKUP_FILE.zip" -Force
            Remove-Item $BACKUP_FILE
            Write-Host "备份成功: $BACKUP_FILE.zip" -ForegroundColor Green
        } else {
            Write-Host "备份成功: $BACKUP_FILE" -ForegroundColor Green
        }
        
        # 删除旧备份
        $cutoffDate = (Get-Date).AddDays(-$RETENTION_DAYS)
        Get-ChildItem -Path $BACKUP_DIR -Filter "postgres_backup_*.sql*" | 
            Where-Object { $_.LastWriteTime -lt $cutoffDate } | 
            Remove-Item -Force
        Write-Host "已清理 $RETENTION_DAYS 天前的备份文件"
    } catch {
        Write-Host "备份失败: $_" -ForegroundColor Red
        exit 1
    }
    
} elseif ($DATABASE_URL -match "^sqlite") {
    # SQLite备份
    $BACKUP_FILE = "$BACKUP_DIR\sqlite_backup_$DATE.db"
    Write-Host "开始备份SQLite数据库..."
    
    # 提取SQLite文件路径
    $DB_PATH = $DATABASE_URL -replace "sqlite:///", ""
    
    if (Test-Path $DB_PATH) {
        try {
            Copy-Item -Path $DB_PATH -Destination $BACKUP_FILE
            
            # 压缩备份文件
            if (Get-Command Compress-Archive -ErrorAction SilentlyContinue) {
                Compress-Archive -Path $BACKUP_FILE -DestinationPath "$BACKUP_FILE.zip" -Force
                Remove-Item $BACKUP_FILE
                Write-Host "备份成功: $BACKUP_FILE.zip" -ForegroundColor Green
            } else {
                Write-Host "备份成功: $BACKUP_FILE" -ForegroundColor Green
            }
            
            # 删除旧备份
            $cutoffDate = (Get-Date).AddDays(-$RETENTION_DAYS)
            Get-ChildItem -Path $BACKUP_DIR -Filter "sqlite_backup_*.db*" | 
                Where-Object { $_.LastWriteTime -lt $cutoffDate } | 
                Remove-Item -Force
            Write-Host "已清理 $RETENTION_DAYS 天前的备份文件"
        } catch {
            Write-Host "备份失败: $_" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "错误: 数据库文件不存在: $DB_PATH" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "错误: 不支持的数据库类型" -ForegroundColor Red
    exit 1
}

Write-Host "备份完成" -ForegroundColor Green
