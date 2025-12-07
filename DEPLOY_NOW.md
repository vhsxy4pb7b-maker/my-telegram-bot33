# 🚀 立即部署到 Railway - 步骤指南

## 当前状态检查

✅ 项目已准备好 Railway 部署：
- ✅ `railway.json` - Railway 配置文件
- ✅ `Procfile` - 启动命令
- ✅ `requirements.txt` - Python 依赖
- ✅ `config.yaml.example` - 配置文件示例

## 📋 部署步骤

### 步骤 1: 准备代码（如果还没推送到 GitHub）

```bash
# 检查 Git 状态
git status

# 如果还没有初始化 Git
git init
git add .
git commit -m "准备 Railway 部署"

# 创建 GitHub 仓库并推送
# 1. 在 GitHub 创建新仓库
# 2. 然后执行：
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

### 步骤 2: 在 Railway 创建项目

1. **访问 Railway**: https://railway.app
2. **登录**: 使用 GitHub 账号登录
3. **创建项目**:
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway 会自动开始部署

### 步骤 3: 添加 PostgreSQL 数据库

1. 在项目页面点击 **"New"** 按钮
2. 选择 **"Database"** → **"Add PostgreSQL"**
3. Railway 会自动创建数据库并设置 `DATABASE_URL` 环境变量

### 步骤 4: 配置环境变量

在 Railway 项目页面：

1. 点击你的服务（不是数据库）
2. 点击 **"Variables"** 标签
3. 点击 **"New Variable"** 添加以下变量：

#### 必需的环境变量：

```
FACEBOOK_APP_ID=你的Facebook应用ID
FACEBOOK_APP_SECRET=你的Facebook应用密钥
FACEBOOK_ACCESS_TOKEN=你的Facebook访问令牌
FACEBOOK_VERIFY_TOKEN=你的Facebook验证令牌
OPENAI_API_KEY=你的OpenAI API密钥
TELEGRAM_BOT_TOKEN=你的Telegram Bot令牌
TELEGRAM_CHAT_ID=你的Telegram聊天ID
SECRET_KEY=你的密钥（使用: python -c "import secrets; print(secrets.token_urlsafe(32))"）
```

#### 服务器配置（Railway 自动设置，但可以手动添加）：

```
HOST=0.0.0.0
PORT=$PORT
DEBUG=false
```

#### 可选配置：

```
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
INSTAGRAM_ACCESS_TOKEN=你的Instagram令牌（如果使用）
INSTAGRAM_USER_ID=你的Instagram用户ID（如果使用）
```

### 步骤 5: 运行数据库迁移

#### 方式 1: 使用 Railway CLI（推荐）

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 链接到项目（在项目目录中执行）
railway link

# 运行数据库迁移
railway run alembic upgrade head
```

#### 方式 2: 在 Railway Shell 中运行

1. 在 Railway 项目页面
2. 点击你的服务
3. 点击 **"Shell"** 标签
4. 运行：
```bash
alembic upgrade head
```

### 步骤 6: 获取部署 URL

1. 在项目页面点击你的服务
2. 点击 **"Settings"** → **"Networking"**
3. 查看 **"Public Domain"**，你会看到类似：
   - `your-service-name.up.railway.app`

### 步骤 7: 配置 Facebook Webhook

1. 打开 Facebook 开发者控制台
2. 进入你的应用设置
3. 配置 Webhook：
   - **Webhook URL**: `https://your-service-name.up.railway.app/webhook`
   - **Verify Token**: 使用你在环境变量中设置的 `FACEBOOK_VERIFY_TOKEN`
   - **订阅事件**: 选择 `messages`, `messaging_postbacks`, `feed`

### 步骤 8: 验证部署

访问以下 URL 验证：

- **健康检查**: `https://your-service-name.up.railway.app/health`
- **API 文档**: `https://your-service-name.up.railway.app/docs`
- **统计接口**: `https://your-service-name.up.railway.app/statistics/daily`

## ✅ 部署检查清单

### 部署前
- [ ] 代码已推送到 GitHub
- [ ] Railway 账号已创建
- [ ] 项目已在 Railway 创建
- [ ] PostgreSQL 数据库已添加
- [ ] 所有环境变量已配置

### 部署后
- [ ] 服务正常运行（查看 Railway 日志）
- [ ] 数据库迁移已运行
- [ ] 健康检查通过
- [ ] API 文档可访问
- [ ] Facebook Webhook 已配置

## 🔧 常见问题

### 1. 部署失败

**检查日志**:
- 在 Railway 项目页面查看部署日志
- 检查是否有错误信息

**常见原因**:
- 环境变量未配置
- 依赖安装失败
- 端口配置错误

### 2. 数据库连接失败

**解决方案**:
- 确认 PostgreSQL 服务已添加
- 检查 `DATABASE_URL` 环境变量
- 运行数据库迁移

### 3. 服务无法启动

**检查**:
- 查看 Railway 日志
- 验证所有必需的环境变量已设置
- 确认启动命令正确（使用 `$PORT`）

## 📝 下一步

部署完成后：

1. **测试 Webhook**: 发送测试消息到 Facebook
2. **查看统计**: 访问统计接口查看数据
3. **配置页面设置**: 使用 `configure_page_auto_reply.py` 配置页面自动回复
4. **监控日志**: 定期查看 Railway 日志确保正常运行

## 🆘 需要帮助？

如果遇到问题：

1. **查看 Railway 日志**: 在项目页面查看详细错误信息
2. **检查环境变量**: 确保所有必需变量已设置
3. **参考文档**: 
   - [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - 完整部署指南
   - [QUICK_RAILWAY_DEPLOY.md](QUICK_RAILWAY_DEPLOY.md) - 快速部署

---

**准备好了吗？按照上述步骤开始部署！** 🚀


