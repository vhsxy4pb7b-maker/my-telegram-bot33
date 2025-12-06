# 系统使用指南

## 🚀 快速开始

### 1. 访问 API 文档

在浏览器中打开：**http://localhost:8000/docs**

您将看到 Swagger UI 界面，显示所有可用的 API 端点。

### 2. 可用的 API 端点

#### 系统端点
- **GET /** - 获取系统信息
- **GET /health** - 健康检查

#### Facebook Webhook
- **GET /webhook** - Facebook Webhook 验证
- **POST /webhook** - 接收 Facebook 消息事件

#### Telegram Bot
- **POST /telegram/webhook** - 接收 Telegram 消息和命令

---

## 🧪 测试系统功能

### 测试 1: 系统信息

在 API 文档中：
1. 找到 **GET /** 端点
2. 点击 "Try it out"
3. 点击 "Execute"
4. 查看响应：应该返回系统信息

**预期响应：**
```json
{
  "message": "Facebook 客服自动化系统",
  "version": "1.0.0",
  "status": "running"
}
```

### 测试 2: 健康检查

1. 找到 **GET /health** 端点
2. 点击 "Try it out" → "Execute"

**预期响应：**
```json
{
  "status": "healthy"
}
```

### 测试 3: Facebook Webhook 验证

1. 找到 **GET /webhook** 端点
2. 点击 "Try it out"
3. 在参数中输入：
   - `hub.mode`: `subscribe`
   - `hub.verify_token`: `.env` 文件中的 `FACEBOOK_VERIFY_TOKEN` 值
   - `hub.challenge`: `test_challenge_123`
4. 点击 "Execute"

**预期响应：** 应该返回 `test_challenge_123`

---

## 🔑 配置 API 密钥后的功能

配置 API 密钥后，系统将能够：

### Facebook 消息处理流程

1. **接收消息**
   - Facebook 发送 Webhook 到 `/webhook`
   - 系统解析消息类型（广告/私信/评论）

2. **AI 自动回复**
   - 使用 OpenAI API 生成智能回复
   - 自动发送回复到 Facebook

3. **资料收集**
   - 自动提取客户信息（姓名、邮箱、电话等）
   - 验证和清洗数据

4. **智能过滤**
   - 关键词过滤（垃圾信息、屏蔽词）
   - 情感分析
   - 优先级判断

5. **Telegram 通知**
   - 符合条件的消息发送到 Telegram
   - 等待人工审核

6. **审核处理**
   - 通过 Telegram Bot 命令审核
   - `/approve_{id}` - 通过
   - `/reject_{id}` - 拒绝
   - `/review_{id}` - 查看详情

---

## 📝 配置 API 密钥步骤

### 方法 1: 使用配置工具

```bash
python configure_api_keys.py
```

按照提示输入：
1. Facebook API 配置
2. OpenAI API 密钥
3. Telegram Bot 配置

### 方法 2: 手动编辑 .env 文件

打开 `.env` 文件，替换以下值：

```env
# Facebook API
FACEBOOK_APP_ID=你的应用ID
FACEBOOK_APP_SECRET=你的应用密钥
FACEBOOK_ACCESS_TOKEN=你的访问令牌
FACEBOOK_VERIFY_TOKEN=你的验证令牌

# OpenAI API
OPENAI_API_KEY=sk-你的密钥

# Telegram Bot
TELEGRAM_BOT_TOKEN=你的Bot令牌
TELEGRAM_CHAT_ID=你的聊天ID
```

---

## 🔧 配置 Facebook Webhook

配置 API 密钥后，需要在 Facebook Developer Console 设置 Webhook：

1. **访问 Facebook Developers**
   - https://developers.facebook.com/
   - 选择您的应用

2. **配置 Webhook**
   - 进入"产品" → "Messenger" → "设置"
   - Webhook URL: `https://your-domain.com/webhook`
   - 验证令牌: 使用 `.env` 中的 `FACEBOOK_VERIFY_TOKEN`
   - 订阅事件: `messages`, `messaging_postbacks`, `feed`

3. **测试 Webhook**
   - 在 API 文档中测试 `/webhook` 端点
   - 或发送测试消息到您的 Facebook 页面

---

## 🔧 配置 Telegram Bot

1. **创建 Bot**
   - 在 Telegram 搜索 `@BotFather`
   - 发送 `/newbot` 创建 Bot
   - 复制返回的 Token

2. **设置 Webhook（可选）**
   ```bash
   curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-domain.com/telegram/webhook"
   ```

3. **获取 Chat ID**
   - 发送消息给 Bot
   - 访问: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - 在返回的 JSON 中找到 `chat.id`

---

## 📊 查看系统数据

### 查看数据库

SQLite 数据库文件：`facebook_customer_service.db`

可以使用 SQLite 工具查看：
- DB Browser for SQLite
- 或使用 Python：
  ```python
  import sqlite3
  conn = sqlite3.connect('facebook_customer_service.db')
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  print(cursor.fetchall())
  ```

### 数据库表结构

- **customers** - 客户信息
- **conversations** - 对话记录
- **collected_data** - 收集的资料
- **reviews** - 审核记录
- **integration_logs** - 集成日志

---

## 🐛 故障排除

### 服务无法启动

1. 检查端口是否被占用：
   ```bash
   netstat -ano | findstr :8000
   ```

2. 检查依赖是否安装：
   ```bash
   python verify_setup.py
   ```

3. 查看错误日志：
   - 检查终端输出的错误信息

### API 密钥错误

1. 验证密钥是否正确：
   - 检查 `.env` 文件中的值
   - 确认没有多余的空格或引号

2. 测试 API 连接：
   - 在 API 文档中测试相关端点
   - 查看错误响应

### 数据库连接失败

1. 检查数据库文件：
   ```bash
   Test-Path facebook_customer_service.db
   ```

2. 重新初始化：
   ```bash
   python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
   ```

---

## 📚 更多资源

- **API 文档**: http://localhost:8000/docs
- **系统文档**: 查看 `README.md`
- **配置指南**: 查看 `QUICK_CONFIG.md`
- **API 密钥**: 查看 `API_KEYS_GUIDE.md`

---

## 🎯 下一步

1. ✅ **系统已启动** - 服务正在运行
2. 📖 **查看 API 文档** - 了解所有可用功能
3. 🔑 **配置 API 密钥** - 启用完整功能
4. 🧪 **测试功能** - 通过 API 文档测试端点
5. 🚀 **开始使用** - 配置 Webhook 开始接收消息

祝您使用愉快！

