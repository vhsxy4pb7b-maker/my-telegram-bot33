# 本地部署指南（不使用 Docker）

## 📋 前提条件

- Python 3.9+ 已安装
- PostgreSQL 已安装并运行
- 所有 API 密钥已准备

## 🚀 快速部署步骤

### 步骤 1: 配置环境变量

```powershell
# 如果 .env 文件不存在，从示例文件创建
if (-not (Test-Path .env)) {
    Copy-Item env.example .env
    Write-Host "✅ .env 文件已创建，请编辑它填入您的配置"
} else {
    Write-Host "ℹ️  .env 文件已存在"
}
```

然后编辑 `.env` 文件，填入所有必需的配置。

### 步骤 2: 创建虚拟环境（如果还没有）

```powershell
# 检查虚拟环境
if (-not (Test-Path venv)) {
    python -m venv venv
    Write-Host "✅ 虚拟环境已创建"
}

# 激活虚拟环境
.\venv\Scripts\Activate.ps1
```

### 步骤 3: 安装依赖

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 4: 配置数据库

确保 PostgreSQL 正在运行，然后创建数据库：

```sql
-- 在 PostgreSQL 中执行
CREATE DATABASE facebook_customer_service;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE facebook_customer_service TO your_user;
```

### 步骤 5: 初始化数据库

```powershell
# 运行数据库迁移
alembic upgrade head

# 如果迁移失败，直接创建表
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 步骤 6: 配置业务规则

```powershell
# 如果 config.yaml 不存在，从示例创建
if (-not (Test-Path config.yaml)) {
    Copy-Item config.yaml.example config.yaml
    Write-Host "✅ config.yaml 已创建，请编辑它配置业务规则"
}
```

### 步骤 7: 启动服务

```powershell
# 方式 1: 使用启动脚本
python run.py

# 方式 2: 直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 步骤 8: 验证部署

打开浏览器访问：
- 健康检查: http://localhost:8000/health
- API 文档: http://localhost:8000/docs
- 统计接口: http://localhost:8000/statistics/daily

## 📝 必需配置项

在 `.env` 文件中必须配置以下项：

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/facebook_customer_service

# Facebook（必需）
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token

# OpenAI（必需）
OPENAI_API_KEY=your_openai_key

# Telegram（必需）
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 安全（必需）
SECRET_KEY=your_secret_key
```

## 🔧 常用命令

```powershell
# 查看日志（如果使用 run.py）
# 日志会直接输出到控制台

# 停止服务
# 按 Ctrl+C

# 检查服务状态
curl http://localhost:8000/health

# 查看统计
python view_statistics.py
```

## ⚠️ 常见问题

### 1. 端口被占用

```powershell
# 检查端口占用
netstat -ano | findstr :8000

# 修改端口（在 .env 文件中）
PORT=8001
```

### 2. 数据库连接失败

- 检查 PostgreSQL 是否运行
- 验证 `DATABASE_URL` 配置
- 检查数据库用户权限

### 3. 模块导入错误

```powershell
# 确保虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 重新安装依赖
pip install -r requirements.txt
```

## 📚 下一步

部署完成后，请：
1. 配置 Facebook Webhook
2. 测试 AI 自动回复
3. 配置页面自动回复设置
4. 查看统计数据

详细文档请参考：
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 完整部署指南
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - 快速部署
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 部署检查清单

