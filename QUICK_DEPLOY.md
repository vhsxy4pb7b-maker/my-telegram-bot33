# 快速部署指南

## 🚀 5分钟快速部署

### 方式 1: Docker Compose（最简单）

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入所有配置

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f app

# 4. 验证部署
curl http://localhost:8000/health
```

### 方式 2: 本地部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
# 编辑 .env 文件

# 3. 初始化数据库
alembic upgrade head

# 4. 启动服务
python run.py
```

## ✅ 验证部署

访问以下 URL：

- 健康检查: http://localhost:8000/health
- API 文档: http://localhost:8000/docs
- 统计接口: http://localhost:8000/statistics/daily

## 📝 必需配置

### 最低配置（.env）

```env
DATABASE_URL=postgresql://user:password@localhost:5432/facebook_customer_service
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
OPENAI_API_KEY=your_openai_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
SECRET_KEY=your_secret_key
```

## 🔧 常用命令

```bash
# Docker Compose
docker-compose up -d          # 启动服务
docker-compose down           # 停止服务
docker-compose logs -f app    # 查看日志
docker-compose restart app    # 重启服务

# 数据库迁移
alembic upgrade head         # 升级数据库
alembic downgrade -1         # 回退一个版本

# 查看统计
python view_statistics.py    # 查看统计数据
```

## 📚 详细文档

完整部署指南请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

