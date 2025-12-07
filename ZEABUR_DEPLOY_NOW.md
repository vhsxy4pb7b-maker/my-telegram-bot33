# 🚀 Zeabur 部署 - 立即执行

## 📋 当前状态
- ✅ 代码已推送到 GitHub: https://github.com/vhsxy4pb7b-maker/my-telegram-bot33
- ✅ 准备在 Zeabur 部署

## 🎯 分步执行指南

### 第一步：在 Zeabur 创建项目（2分钟）

1. **打开浏览器**，访问: https://zeabur.com
2. **登录**: 使用 GitHub 账号登录
3. **创建项目**:
   - 点击 "New Project" 或 "+" 按钮
   - 选择 "Import from GitHub" 或 "GitHub"
   - 如果首次使用，授权 Zeabur 访问 GitHub
   - 在仓库列表中找到并选择: **`vhsxy4pb7b-maker/my-telegram-bot33`**
   - Zeabur 会自动检测项目类型并开始部署

**等待**: 部署过程通常需要 2-5 分钟

**完成后告诉我**: "项目已创建" 或 "部署中"

---

### 第二步：添加 PostgreSQL 数据库（1分钟）

1. 在项目页面，点击 **"Add Service"** 或 **"+"** 按钮
2. 选择 **"Database"**
3. 选择 **"PostgreSQL"**
4. Zeabur 会自动创建数据库并设置 `DATABASE_URL`

**完成后告诉我**: "数据库已添加"

---

### 第三步：配置环境变量（5分钟）

1. 在项目页面，点击你的**应用服务**（不是数据库服务）
2. 进入 **"Environment Variables"** 或 **"Variables"** 标签
3. 点击 **"Add Variable"** 或 **"+"** 按钮
4. **逐个添加以下 8 个变量**：

#### 必需变量列表：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `FACEBOOK_APP_ID` | 你的Facebook应用ID | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_APP_SECRET` | 你的Facebook应用密钥 | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_ACCESS_TOKEN` | 你的Facebook访问令牌 | 从 Facebook 开发者控制台获取 |
| `FACEBOOK_VERIFY_TOKEN` | `my_verify_token_123` | 自定义字符串（用于 Webhook 验证） |
| `OPENAI_API_KEY` | 你的OpenAI API密钥 | 从 OpenAI 平台获取 |
| `TELEGRAM_BOT_TOKEN` | 你的Telegram Bot令牌 | 从 @BotFather 获取 |
| `TELEGRAM_CHAT_ID` | 你的Telegram聊天ID | 你的 Telegram 用户 ID 或群组 ID |
| `SECRET_KEY` | `YB-Y7XHm6JuFqMl1fJOuFRLgUEJZPG2x5lQnVC_tJ2U` | 已生成，直接使用 |

**重要提示**:
- `DATABASE_URL` 由 Zeabur 自动设置，**不需要手动添加**
- `FACEBOOK_VERIFY_TOKEN` 可以是任意字符串，但要记住它（稍后配置 Webhook 时需要）
- 添加每个变量后点击保存

**完成后告诉我**: "环境变量已配置"

---

### 第四步：运行数据库迁移（2分钟）

#### 方式 1: 使用 Zeabur CLI（推荐）

```bash
# 1. 安装 Zeabur CLI（如果还没安装）
npm i -g @zeabur/cli

# 2. 登录
zeabur login

# 3. 在项目目录中链接项目
cd C:\Users\zhuanqian\Desktop\无极1
zeabur link
# 选择你的项目

# 4. 运行数据库迁移
zeabur exec alembic upgrade head
```

#### 方式 2: 使用 Zeabur Web Terminal

1. 在 Zeabur 项目页面，点击你的应用服务
2. 点击 **"Terminal"** 或 **"Console"** 标签
3. 运行：
```bash
alembic upgrade head
```

**完成后告诉我**: "数据库迁移已完成"

---

### 第五步：获取域名（1分钟）

1. 在 Zeabur 项目页面，点击你的应用服务
2. 查看 **"Domains"** 或 **"URL"** 部分
3. 你会看到类似：
   ```
   your-service.zeabur.app
   ```
4. **复制这个 URL**

**完成后告诉我**: "域名已获取: xxx.zeabur.app"

---

### 第六步：配置 Facebook Webhook（3分钟）

1. 打开 [Facebook 开发者控制台](https://developers.facebook.com/)
2. 选择你的应用
3. 进入 **"Webhooks"** 或 **"Messenger"** → **"Webhooks"** 设置
4. 点击 **"Add Callback URL"** 或 **"Edit"**
5. 填写信息：
   - **Callback URL**: `https://你的域名.zeabur.app/webhook`
     （使用步骤 5 中获取的域名）
   - **Verify Token**: 使用你在步骤 3 中设置的 `FACEBOOK_VERIFY_TOKEN` 的值
   - **订阅字段**: 勾选以下事件：
     - ✅ `messages`
     - ✅ `messaging_postbacks`
     - ✅ `feed`
6. 点击 **"Verify and Save"**

**完成后告诉我**: "Webhook 已配置"

---

### 第七步：验证部署（2分钟）

访问以下 URL 验证：

1. **健康检查**:
   ```
   https://你的域名.zeabur.app/health
   ```
   应该返回: `{"status": "healthy"}`

2. **API 文档**:
   ```
   https://你的域名.zeabur.app/docs
   ```
   应该显示 Swagger UI 文档页面

3. **统计接口**:
   ```
   https://你的域名.zeabur.app/statistics/daily
   ```
   应该返回统计数据

**完成后告诉我**: "验证通过" 或 "遇到问题：..."

---

## ✅ 部署检查清单

### 部署前
- [ ] Zeabur 账号已创建
- [ ] GitHub 仓库已推送
- [ ] 所有 API 密钥已准备

### 部署中
- [ ] 项目已在 Zeabur 创建
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

## 🔧 故障排查

### 问题 1: 环境变量错误

**错误**: `facebook_verify_token Field required`

**解决**:
1. 在 Zeabur → Environment Variables
2. 添加所有 8 个必需的环境变量
3. 确保 `FACEBOOK_VERIFY_TOKEN` 已添加
4. Zeabur 会自动重新部署

### 问题 2: 部署失败

**检查**:
- 查看 Zeabur 部署日志
- 确认所有必需的环境变量已设置
- 检查 `requirements.txt` 是否正确

### 问题 3: 数据库连接失败

**解决**:
1. 确认 PostgreSQL 服务已添加
2. 检查 `DATABASE_URL` 是否自动设置
3. 运行数据库迁移: `zeabur exec alembic upgrade head`

### 问题 4: Webhook 验证失败

**检查**:
- 确认 Webhook URL 正确
- 确认 `FACEBOOK_VERIFY_TOKEN` 与 Facebook 设置一致
- 确认服务正在运行

---

## 📝 环境变量快速参考

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

---

## 🆘 需要帮助？

告诉我：
- 你当前在哪一步
- 遇到了什么问题
- 看到了什么错误信息

我会立即帮你解决！

---

## 📚 相关文档

- [ZEABUR_DEPLOYMENT.md](ZEABUR_DEPLOYMENT.md) - 完整 Zeabur 部署指南
- [QUICK_ZEABUR_DEPLOY.md](QUICK_ZEABUR_DEPLOY.md) - 快速部署
- [zeabur_env_vars.txt](zeabur_env_vars.txt) - 环境变量清单


