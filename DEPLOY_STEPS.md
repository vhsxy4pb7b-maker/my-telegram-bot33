# 🚀 Railway 部署步骤 - 详细指南

## 当前状态

✅ **项目已准备好部署**：
- Railway 配置文件已创建（`railway.json`, `Procfile`）
- 依赖文件完整（`requirements.txt`）
- 环境变量清单已准备（`railway_env_vars.txt`）

## 📋 部署流程

### 第一步：准备 Git 仓库

由于 Railway 需要从 GitHub 部署，我们需要先创建 Git 仓库：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交代码
git commit -m "准备 Railway 部署"

# 4. 在 GitHub 创建新仓库（手动操作）
#    - 访问 https://github.com/new
#    - 创建新仓库（不要初始化 README）
#    - 复制仓库 URL

# 5. 连接远程仓库并推送
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 第二步：在 Railway 创建项目

1. **访问 Railway**: https://railway.app
2. **登录**: 点击 "Login" → 使用 GitHub 账号登录
3. **创建项目**:
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 授权 Railway 访问你的 GitHub
   - 选择刚才创建的仓库
   - Railway 会自动开始部署

### 第三步：添加 PostgreSQL 数据库

1. 在 Railway 项目页面，点击 **"New"** 按钮
2. 选择 **"Database"** → **"Add PostgreSQL"**
3. Railway 会自动：
   - 创建 PostgreSQL 数据库
   - 设置 `DATABASE_URL` 环境变量
   - 连接到你的应用

### 第四步：配置环境变量

1. 在 Railway 项目页面，点击你的**应用服务**（不是数据库）
2. 点击 **"Variables"** 标签
3. 点击 **"New Variable"** 添加变量

**参考 `railway_env_vars.txt` 文件，添加以下变量：**

#### 必需变量（必须添加）：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `FACEBOOK_APP_ID` | 你的Facebook应用ID | Facebook 应用 ID |
| `FACEBOOK_APP_SECRET` | 你的Facebook应用密钥 | Facebook 应用密钥 |
| `FACEBOOK_ACCESS_TOKEN` | 你的Facebook访问令牌 | Facebook 访问令牌 |
| `FACEBOOK_VERIFY_TOKEN` | 你的Facebook验证令牌 | Webhook 验证令牌 |
| `OPENAI_API_KEY` | 你的OpenAI API密钥 | OpenAI API 密钥 |
| `TELEGRAM_BOT_TOKEN` | 你的Telegram Bot令牌 | Telegram Bot 令牌 |
| `TELEGRAM_CHAT_ID` | 你的Telegram聊天ID | Telegram 聊天 ID |
| `SECRET_KEY` | `YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U` | 应用密钥（已生成） |

#### 可选变量：

- `OPENAI_MODEL` = `gpt-4`
- `OPENAI_TEMPERATURE` = `0.7`
- `HOST` = `0.0.0.0`
- `PORT` = `$PORT`（Railway 自动设置）
- `DEBUG` = `false`

**注意**：`DATABASE_URL` 由 Railway 自动设置，无需手动添加。

### 第五步：运行数据库迁移

部署完成后，需要运行数据库迁移：

#### 方式 1: 使用 Railway CLI（推荐）

```bash
# 1. 安装 Railway CLI
npm i -g @railway/cli

# 2. 登录
railway login

# 3. 在项目目录中链接项目
cd 无极1
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

### 第六步：获取部署 URL

1. 在 Railway 项目页面，点击你的应用服务
2. 点击 **"Settings"** → **"Networking"**
3. 查看 **"Public Domain"**，你会看到类似：
   ```
   your-service-name.up.railway.app
   ```
4. 复制这个 URL，用于配置 Webhook

### 第七步：配置 Facebook Webhook

1. 打开 [Facebook 开发者控制台](https://developers.facebook.com/)
2. 进入你的应用
3. 进入 **"Webhooks"** 设置
4. 点击 **"Add Callback URL"**
5. 配置：
   - **Callback URL**: `https://your-service-name.up.railway.app/webhook`
   - **Verify Token**: 使用你在环境变量中设置的 `FACEBOOK_VERIFY_TOKEN`
   - **订阅事件**: 勾选以下事件：
     - `messages`
     - `messaging_postbacks`
     - `feed`
6. 点击 **"Verify and Save"**

### 第八步：验证部署

访问以下 URL 验证部署：

1. **健康检查**: 
   ```
   https://your-service-name.up.railway.app/health
   ```
   应该返回：`{"status": "healthy"}`

2. **API 文档**: 
   ```
   https://your-service-name.up.railway.app/docs
   ```
   应该显示 Swagger UI 文档

3. **统计接口**: 
   ```
   https://your-service-name.up.railway.app/statistics/daily
   ```
   应该返回统计数据

## ✅ 部署检查清单

### 部署前
- [ ] Git 仓库已创建并推送
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

## 🔧 查看日志和调试

### 在 Railway 网站查看日志

1. 在项目页面点击你的应用服务
2. 点击 **"Deployments"** 标签
3. 选择最新的部署
4. 查看实时日志

### 使用 Railway CLI 查看日志

```bash
railway logs
railway logs --follow  # 实时日志
```

## 🆘 常见问题

### 1. 部署失败

**检查**：
- 查看 Railway 部署日志
- 确认所有必需的环境变量已设置
- 检查 `requirements.txt` 是否正确

### 2. 数据库连接失败

**解决**：
- 确认 PostgreSQL 服务已添加
- 检查 `DATABASE_URL` 是否自动设置
- 运行数据库迁移：`railway run alembic upgrade head`

### 3. Webhook 验证失败

**检查**：
- 确认 Webhook URL 正确
- 确认 `FACEBOOK_VERIFY_TOKEN` 与 Facebook 设置一致
- 查看 Railway 日志中的错误信息

### 4. 服务无法启动

**检查**：
- 查看 Railway 日志
- 确认 `PORT` 环境变量使用 `$PORT`
- 验证所有必需的环境变量已设置

## 📝 下一步

部署完成后：

1. **测试功能**: 发送测试消息到 Facebook，验证自动回复
2. **配置页面设置**: 使用统计接口查看数据
3. **监控运行**: 定期查看 Railway 日志
4. **设置自定义域名**（可选）: 在 Railway Settings → Networking 配置

## 📚 相关文档

- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - 完整部署指南
- [QUICK_RAILWAY_DEPLOY.md](QUICK_RAILWAY_DEPLOY.md) - 快速部署
- [railway_env_vars.txt](railway_env_vars.txt) - 环境变量清单

---

**准备好了吗？按照步骤开始部署！** 🚀

