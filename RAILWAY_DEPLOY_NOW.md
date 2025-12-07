# 🚀 Railway 部署 - 立即执行

## 📋 快速部署步骤

### 步骤 1: 在 Railway 创建项目（网页操作）

1. **访问**: https://railway.app
2. **点击**: "New Project" 按钮
3. **选择**: "Deploy from GitHub repo"
4. **授权**: 如果首次使用，授权 Railway 访问 GitHub
5. **选择仓库**: `vhsxy4pb7b-maker/my-telegram-bot33`
6. **等待**: Railway 自动开始部署（2-5分钟）

---

### 步骤 2: 添加 PostgreSQL 数据库

1. 在项目页面，点击 **"New"** 按钮
2. 选择 **"Database"** → **"Add PostgreSQL"**
3. Railway 会自动创建并连接数据库

---

### 步骤 3: 配置环境变量

在 Railway 项目页面 → 点击你的应用服务 → "Variables" 标签

**逐个添加以下变量**（点击 "New Variable" 添加）：

```
FACEBOOK_APP_ID = 你的Facebook应用ID
FACEBOOK_APP_SECRET = 你的Facebook应用密钥
FACEBOOK_ACCESS_TOKEN = 你的Facebook访问令牌
FACEBOOK_VERIFY_TOKEN = 你的Facebook验证令牌（自定义字符串）
OPENAI_API_KEY = 你的OpenAI API密钥
TELEGRAM_BOT_TOKEN = 你的Telegram Bot令牌
TELEGRAM_CHAT_ID = 你的Telegram聊天ID
SECRET_KEY = YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U
```

**注意**: `DATABASE_URL` 由 Railway 自动设置，无需手动添加

---

### 步骤 4: 运行数据库迁移

#### 方式 1: 使用 Railway CLI（推荐）

```bash
# 1. 安装 Railway CLI（如果还没安装）
npm i -g @railway/cli

# 2. 登录
railway login

# 3. 在项目目录中链接项目
cd C:\Users\zhuanqian\Desktop\无极1
railway link
# 选择你的项目

# 4. 运行数据库迁移
railway run alembic upgrade head
```

#### 方式 2: 使用 Railway Web Shell

1. 在 Railway 项目页面，点击你的应用服务
2. 点击 **"Shell"** 标签
3. 运行：
```bash
alembic upgrade head
```

---

### 步骤 5: 获取域名

1. 在 Railway 项目页面，点击你的应用服务
2. 点击 **"Settings"** → **"Networking"**
3. 查看 **"Public Domain"**，复制域名（格式: `xxx.up.railway.app`）

---

### 步骤 6: 配置 Facebook Webhook

1. 打开: https://developers.facebook.com/
2. 选择你的应用
3. 进入 **"Webhooks"** 设置
4. 配置：
   - **Callback URL**: `https://你的域名.up.railway.app/webhook`
   - **Verify Token**: 使用环境变量中的 `FACEBOOK_VERIFY_TOKEN`
   - **订阅事件**: `messages`, `messaging_postbacks`, `feed`
5. 点击 **"Verify and Save"**

---

### 步骤 7: 验证部署

访问以下 URL 验证：

- 健康检查: `https://你的域名.up.railway.app/health`
- API 文档: `https://你的域名.up.railway.app/docs`

---

## 🔧 使用辅助脚本

运行以下命令获取交互式帮助：

```bash
python deploy_to_railway.py
```

这个脚本会：
- 检查环境
- 显示配置指南
- 提供 Railway CLI 命令
- 显示检查清单

---

## ⚠️ 常见问题

### 部署失败

**原因**: 通常是因为缺少环境变量

**解决**: 
1. 添加所有必需的环境变量
2. Railway 会自动重新部署

### 数据库连接失败

**解决**: 
1. 确认 PostgreSQL 已添加
2. 运行数据库迁移: `railway run alembic upgrade head`

### Webhook 验证失败

**检查**:
- URL 是否正确
- Verify Token 是否匹配
- 服务是否正常运行

---

## ✅ 完成检查

部署完成后，确认：

- [ ] 服务状态为 "Active"
- [ ] 健康检查返回 `{"status": "healthy"}`
- [ ] API 文档可以访问
- [ ] Facebook Webhook 已验证
- [ ] 可以发送测试消息

---

## 📚 详细文档

- [STEP_BY_STEP_RAILWAY.md](STEP_BY_STEP_RAILWAY.md) - 完整步骤指南
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Railway 完整文档
- [railway_env_vars.txt](railway_env_vars.txt) - 环境变量清单

---

**需要帮助？** 告诉我你当前在哪一步，我会继续协助！


