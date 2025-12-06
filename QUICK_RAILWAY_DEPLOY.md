# Railway 快速部署指南

## 🚀 5分钟快速部署到 Railway

### 步骤 1: 创建 Railway 账号

访问 [railway.app](https://railway.app) 并使用 GitHub 账号登录

### 步骤 2: 创建新项目

1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你的仓库
4. Railway 会自动开始部署

### 步骤 3: 添加 PostgreSQL 数据库

1. 在项目页面点击 "New"
2. 选择 "Database" → "Add PostgreSQL"
3. Railway 会自动设置 `DATABASE_URL`

### 步骤 4: 配置环境变量

在项目页面 → Variables 中添加：

```env
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

# 服务器（Railway 自动设置）
PORT=$PORT
HOST=0.0.0.0
```

### 步骤 5: 运行数据库迁移

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 链接项目
railway link

# 运行迁移
railway run alembic upgrade head
```

### 步骤 6: 获取域名

在项目页面 → Settings → Networking 查看：
- Railway 域名：`your-service.up.railway.app`
- 自动启用 HTTPS

### 步骤 7: 配置 Webhook

在 Facebook 开发者控制台：
- Webhook URL: `https://your-service.up.railway.app/webhook`
- Verify Token: 使用环境变量中的 `FACEBOOK_VERIFY_TOKEN`

## ✅ 验证部署

访问：
- 健康检查: `https://your-service.up.railway.app/health`
- API 文档: `https://your-service.up.railway.app/docs`

## 📝 必需环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `DATABASE_URL` | 数据库连接（Railway 自动提供） | ✅ |
| `FACEBOOK_APP_ID` | Facebook 应用 ID | ✅ |
| `FACEBOOK_APP_SECRET` | Facebook 应用密钥 | ✅ |
| `FACEBOOK_ACCESS_TOKEN` | Facebook 访问令牌 | ✅ |
| `FACEBOOK_VERIFY_TOKEN` | Facebook 验证令牌 | ✅ |
| `OPENAI_API_KEY` | OpenAI API 密钥 | ✅ |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot 令牌 | ✅ |
| `TELEGRAM_CHAT_ID` | Telegram 聊天 ID | ✅ |
| `SECRET_KEY` | 应用密钥 | ✅ |
| `PORT` | 端口（Railway 自动设置） | ✅ |

## 🔧 常用命令

```bash
# 查看日志
railway logs

# 运行命令
railway run python view_statistics.py

# 重启服务
railway restart

# 查看变量
railway variables
```

## 📚 详细文档

完整 Railway 部署指南请查看 [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

