# 🚀 Railway 部署 - 一步步完成指南

## ✅ 已完成步骤

- [x] Git 仓库初始化
- [x] 代码提交到本地
- [x] 推送到 GitHub: https://github.com/vhsxy4pb7b-maker/my-telegram-bot33

## 📋 接下来要完成的步骤

### 步骤 1: 访问 Railway 并登录

1. **打开浏览器**，访问: https://railway.app
2. **点击 "Login"** 或 "Start a New Project"
3. **选择登录方式**: 
   - 点击 "Login with GitHub"
   - 授权 Railway 访问你的 GitHub 账号
   - 完成登录

**验证**: 登录后应该能看到 Railway 仪表板

---

### 步骤 2: 创建新项目

1. 在 Railway 仪表板，点击 **"New Project"** 按钮（通常在右上角或中间）
2. 选择 **"Deploy from GitHub repo"**
3. 如果首次使用，可能需要：
   - 授权 Railway 访问你的 GitHub
   - 选择要授权的仓库（可以选择所有仓库或特定仓库）
4. 在仓库列表中找到并选择: **`vhsxy4pb7b-maker/my-telegram-bot33`**
5. Railway 会自动开始部署

**验证**: 你应该能看到部署进度，Railway 正在构建你的项目

**等待时间**: 通常需要 2-5 分钟

---

### 步骤 3: 添加 PostgreSQL 数据库

1. 在项目页面，点击 **"New"** 按钮（通常在左侧或顶部）
2. 选择 **"Database"**
3. 选择 **"Add PostgreSQL"**
4. Railway 会自动：
   - 创建 PostgreSQL 数据库
   - 设置 `DATABASE_URL` 环境变量
   - 连接到你的应用

**验证**: 在项目页面应该能看到两个服务：
- 你的应用服务
- PostgreSQL 数据库服务

---

### 步骤 4: 配置环境变量

1. 在项目页面，点击你的**应用服务**（不是数据库服务）
2. 点击 **"Variables"** 标签
3. 点击 **"New Variable"** 按钮
4. 逐个添加以下变量：

#### 必需变量列表：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `FACEBOOK_APP_ID` | 你的Facebook应用ID | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_APP_SECRET` | 你的Facebook应用密钥 | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_ACCESS_TOKEN` | 你的Facebook访问令牌 | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_VERIFY_TOKEN` | 你的Facebook验证令牌 | 自定义一个字符串（用于 Webhook 验证） |
| `OPENAI_API_KEY` | 你的OpenAI API密钥 | 从 OpenAI 平台获取 |
| `TELEGRAM_BOT_TOKEN` | 你的Telegram Bot令牌 | 从 @BotFather 获取 |
| `TELEGRAM_CHAT_ID` | 你的Telegram聊天ID | 你的 Telegram 用户 ID 或群组 ID |
| `SECRET_KEY` | `YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U` | 已生成，直接使用 |

#### 可选变量（可以稍后添加）：

- `OPENAI_MODEL` = `gpt-4`
- `OPENAI_TEMPERATURE` = `0.7`
- `HOST` = `0.0.0.0`
- `PORT` = `$PORT`（Railway 自动设置，通常不需要手动添加）
- `DEBUG` = `false`

**注意**: 
- `DATABASE_URL` 由 Railway 自动设置，**不需要手动添加**
- 添加每个变量后点击 "Add" 保存

**验证**: 在 Variables 列表中应该能看到所有添加的变量

---

### 步骤 5: 等待部署完成

1. 在项目页面，点击你的应用服务
2. 查看 **"Deployments"** 标签
3. 等待部署状态变为 **"Active"** 或 **"Success"**

**如果部署失败**:
- 点击部署记录查看日志
- 检查是否有错误信息
- 常见问题：
  - 缺少必需的环境变量
  - 依赖安装失败
  - 端口配置错误

---

### 步骤 6: 运行数据库迁移

部署完成后，需要运行数据库迁移来创建表结构。

#### 方式 1: 使用 Railway CLI（推荐）

```bash
# 1. 安装 Railway CLI（如果还没安装）
npm i -g @railway/cli

# 2. 登录 Railway
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
3. 在终端中运行：
```bash
alembic upgrade head
```

**验证**: 应该看到迁移成功的信息，没有错误

---

### 步骤 7: 获取部署 URL

1. 在 Railway 项目页面，点击你的应用服务
2. 点击 **"Settings"** 标签
3. 找到 **"Networking"** 部分
4. 查看 **"Public Domain"**，你会看到类似：
   ```
   your-service-name.up.railway.app
   ```
5. **复制这个 URL**，稍后用于配置 Webhook

**如果没有看到 Public Domain**:
- 点击 **"Generate Domain"** 按钮
- Railway 会自动生成一个域名

**验证**: 访问 `https://your-service-name.up.railway.app/health` 应该返回：
```json
{"status": "healthy"}
```

---

### 步骤 8: 配置 Facebook Webhook

1. **打开 Facebook 开发者控制台**: https://developers.facebook.com/
2. **选择你的应用**
3. 在左侧菜单找到 **"Webhooks"** 或 **"Messenger"** → **"Webhooks"**
4. 点击 **"Add Callback URL"** 或 **"Edit"**
5. 填写信息：
   - **Callback URL**: `https://your-service-name.up.railway.app/webhook`
     （替换为步骤 7 中获取的实际域名）
   - **Verify Token**: 使用你在步骤 4 中设置的 `FACEBOOK_VERIFY_TOKEN` 的值
   - **订阅字段**: 勾选以下事件：
     - ✅ `messages`
     - ✅ `messaging_postbacks`
     - ✅ `feed`
6. 点击 **"Verify and Save"**

**验证**: 
- Webhook 应该显示为 "Verified" 状态
- 如果验证失败，检查：
  - URL 是否正确
  - Verify Token 是否匹配
  - 服务是否正常运行

---

### 步骤 9: 测试部署

访问以下 URL 验证部署：

1. **健康检查**:
   ```
   https://your-service-name.up.railway.app/health
   ```
   应该返回: `{"status": "healthy"}`

2. **API 文档**:
   ```
   https://your-service-name.up.railway.app/docs
   ```
   应该显示 Swagger UI 文档页面

3. **统计接口**:
   ```
   https://your-service-name.up.railway.app/statistics/daily
   ```
   应该返回统计数据（可能是空的，如果还没有数据）

---

### 步骤 10: 测试完整流程

1. **发送测试消息**:
   - 在 Facebook 页面发送一条消息
   - 系统应该自动回复

2. **查看日志**:
   - 在 Railway 项目页面查看应用日志
   - 确认消息被接收和处理

3. **查看统计**:
   - 访问统计接口查看数据
   - 或使用 `view_statistics.py` 脚本

---

## 🔧 故障排查

### 问题 1: 部署失败

**检查**:
- 查看 Railway 部署日志
- 确认所有必需的环境变量已设置
- 检查 `requirements.txt` 是否正确

**解决**:
- 修复错误后，Railway 会自动重新部署
- 或手动点击 "Redeploy"

### 问题 2: 数据库连接失败

**检查**:
- 确认 PostgreSQL 服务已添加
- 检查 `DATABASE_URL` 是否自动设置
- 运行数据库迁移

**解决**:
```bash
railway run alembic upgrade head
```

### 问题 3: Webhook 验证失败

**检查**:
- 确认 Webhook URL 正确
- 确认 `FACEBOOK_VERIFY_TOKEN` 与 Facebook 设置一致
- 确认服务正在运行

**解决**:
- 检查 Railway 日志
- 重新验证 Webhook

### 问题 4: 服务无法启动

**检查**:
- 查看 Railway 日志
- 确认所有必需的环境变量已设置
- 验证启动命令正确

---

## 📝 部署检查清单

### 部署前
- [ ] Railway 账号已创建
- [ ] GitHub 仓库已推送
- [ ] 所有 API 密钥已准备

### 部署中
- [ ] 项目已在 Railway 创建
- [ ] PostgreSQL 数据库已添加
- [ ] 所有环境变量已配置
- [ ] 部署成功完成

### 部署后
- [ ] 数据库迁移已运行
- [ ] 健康检查通过
- [ ] API 文档可访问
- [ ] Facebook Webhook 已配置
- [ ] 测试消息可以正常接收和回复

---

## 🎉 完成！

如果所有步骤都完成，你的系统应该已经：
- ✅ 部署到 Railway
- ✅ 数据库已配置
- ✅ Webhook 已连接
- ✅ 可以接收和处理消息

## 📚 相关文档

- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - 完整部署指南
- [railway_env_vars.txt](railway_env_vars.txt) - 环境变量清单
- [DEPLOY_STEPS.md](DEPLOY_STEPS.md) - 详细部署步骤

---

**需要帮助？** 如果在任何步骤遇到问题，请告诉我具体在哪一步，我会帮你解决！


