# 系统设置说明

## ✅ 已完成的步骤

1. ✅ 项目结构已创建
2. ✅ 依赖文件已准备（requirements.txt）
3. ✅ 配置文件模板已创建（.env, config.yaml）
4. ✅ 数据库迁移文件已创建

## 📋 需要您手动完成的步骤

### 1. 安装依赖（如果还未安装）

```bash
python -m pip install -r requirements.txt
```

### 2. 配置 .env 文件

编辑 `.env` 文件，填入真实的配置信息：

**必需配置：**
- `DATABASE_URL`: PostgreSQL 数据库连接字符串
  - 格式：`postgresql://用户名:密码@主机:端口/数据库名`
  - 示例：`postgresql://postgres:password@localhost:5432/facebook_customer_service`
  
- `FACEBOOK_APP_ID`: Facebook 应用 ID
- `FACEBOOK_APP_SECRET`: Facebook 应用密钥
- `FACEBOOK_ACCESS_TOKEN`: Facebook 访问令牌
- `FACEBOOK_VERIFY_TOKEN`: Webhook 验证令牌（自定义）

- `OPENAI_API_KEY`: OpenAI API 密钥

- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token（通过 @BotFather 获取）
- `TELEGRAM_CHAT_ID`: Telegram 聊天 ID（接收通知的群组或个人聊天）

- `SECRET_KEY`: 用于加密的密钥（随机生成）

**可选配置：**
- `MANYCHAT_API_KEY`: ManyChat API 密钥（如果使用）
- `BOTCAKE_API_KEY`: Botcake API 密钥（如果使用）

### 3. 创建 PostgreSQL 数据库

```sql
CREATE DATABASE facebook_customer_service;
```

### 4. 运行数据库迁移

```bash
# 如果 alembic 命令可用
alembic upgrade head

# 或者使用 Python 直接运行（如果数据库已配置）
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 5. 配置 Facebook Webhook

1. 在 Facebook Developer Console 中：
   - Webhook URL: `https://your-domain.com/webhook`
   - 验证令牌: 使用 `.env` 中的 `FACEBOOK_VERIFY_TOKEN`
   - 订阅事件: `messages`, `messaging_postbacks`, `feed`

### 6. 配置 Telegram Bot

1. 通过 @BotFather 创建 Bot 并获取 Token
2. 将 Token 填入 `.env` 文件
3. 获取 Chat ID（可以通过发送消息给 Bot，然后访问 `https://api.telegram.org/bot<TOKEN>/getUpdates`）

### 7. 启动服务

```bash
python run.py
```

或

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔍 验证安装

1. 访问 `http://localhost:8000/health` - 应该返回 `{"status": "healthy"}`
2. 访问 `http://localhost:8000/docs` - 查看 API 文档
3. 检查日志输出，确认没有错误

## ⚠️ 常见问题

### 数据库连接失败
- 确保 PostgreSQL 服务正在运行
- 检查 `DATABASE_URL` 配置是否正确
- 确保数据库已创建

### API 密钥错误
- 检查所有 API 密钥是否有效
- 确保密钥未过期
- 检查权限设置

### 模块导入错误
- 确保已安装所有依赖：`python -m pip install -r requirements.txt`
- 检查 Python 版本是否为 3.9+

## 📝 下一步

配置完成后，系统将能够：
1. 接收 Facebook 消息
2. 自动生成 AI 回复
3. 收集客户资料
4. 发送 Telegram 审核通知
5. 处理人工审核

祝使用愉快！


