# Zeabur 快速部署指南

## 🚀 5分钟快速部署到 Zeabur

### 步骤 1: 创建项目

1. 访问: https://zeabur.com
2. 使用 GitHub 账号登录
3. 点击 "New Project" 或 "+"
4. 选择 "Import from GitHub"
5. 选择仓库: `vhsxy4pb7b-maker/my-telegram-bot33`
6. Zeabur 会自动开始部署

### 步骤 2: 添加数据库

1. 在项目页面，点击 "Add Service" 或 "+"
2. 选择 "Database" → "PostgreSQL"
3. Zeabur 会自动设置 `DATABASE_URL`

### 步骤 3: 配置环境变量

在项目页面 → 应用服务 → Environment Variables 添加：

```
FACEBOOK_APP_ID=你的Facebook应用ID
FACEBOOK_APP_SECRET=你的Facebook应用密钥
FACEBOOK_ACCESS_TOKEN=你的Facebook访问令牌
FACEBOOK_VERIFY_TOKEN=my_verify_token_123
OPENAI_API_KEY=你的OpenAI API密钥
TELEGRAM_BOT_TOKEN=你的Telegram Bot令牌
TELEGRAM_CHAT_ID=你的Telegram聊天ID
SECRET_KEY=YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U
```

### 步骤 4: 运行数据库迁移

```bash
# 安装 Zeabur CLI
npm i -g @zeabur/cli

# 登录并链接
zeabur login
zeabur link

# 运行迁移
zeabur exec alembic upgrade head
```

### 步骤 5: 获取域名

在项目页面 → Domains 查看：
- Zeabur 域名：`your-service.zeabur.app`
- 自动启用 HTTPS

### 步骤 6: 配置 Webhook

在 Facebook 开发者控制台：
- Webhook URL: `https://your-service.zeabur.app/webhook`
- Verify Token: 使用环境变量中的 `FACEBOOK_VERIFY_TOKEN`

## ✅ 验证部署

访问：
- 健康检查: `https://your-service.zeabur.app/health`
- API 文档: `https://your-service.zeabur.app/docs`

## 📝 必需环境变量

| 变量名 | 说明 |
|--------|------|
| `FACEBOOK_APP_ID` | Facebook 应用 ID |
| `FACEBOOK_APP_SECRET` | Facebook 应用密钥 |
| `FACEBOOK_ACCESS_TOKEN` | Facebook 访问令牌 |
| `FACEBOOK_VERIFY_TOKEN` | Webhook 验证令牌 |
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot 令牌 |
| `TELEGRAM_CHAT_ID` | Telegram 聊天 ID |
| `SECRET_KEY` | 应用密钥 |

## 🔧 常用命令

```bash
# 查看日志
zeabur logs

# 运行命令
zeabur exec python view_statistics.py

# 重启服务
zeabur restart
```

## 📚 详细文档

完整 Zeabur 部署指南请查看 [ZEABUR_DEPLOYMENT.md](ZEABUR_DEPLOYMENT.md)


