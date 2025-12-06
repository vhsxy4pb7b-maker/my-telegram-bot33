# 快速启动指南

## 前置条件

1. Python 3.9+ 已安装
2. PostgreSQL 数据库已安装并运行
3. 已获取所有必要的 API 密钥

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件（参考 `.env.example`）：

```bash
# 必需配置
DATABASE_URL=postgresql://user:password@localhost:5432/facebook_customer_service
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
OPENAI_API_KEY=your_openai_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
SECRET_KEY=your_secret_key

# 可选配置
MANYCHAT_API_KEY=your_manychat_key
BOTCAKE_API_KEY=your_botcake_key
```

### 3. 配置业务规则

创建 `config.yaml` 文件（参考 `config.yaml.example`）

### 4. 初始化数据库

```bash
# 生成迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 5. 启动服务

```bash
python run.py
```

或

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 验证安装

1. 访问 `http://localhost:8000/health` 应该返回 `{"status": "healthy"}`
2. 访问 `http://localhost:8000/docs` 查看 API 文档

## 配置 Webhook

### Facebook Webhook

1. Webhook URL: `https://your-domain.com/webhook`
2. 验证令牌: 使用 `.env` 中的 `FACEBOOK_VERIFY_TOKEN`
3. 订阅事件: `messages`, `messaging_postbacks`, `feed`

### Telegram Webhook

1. Webhook URL: `https://your-domain.com/telegram/webhook`
2. 通过 Telegram Bot API 设置

## 常见问题

### 数据库连接失败

- 检查 PostgreSQL 是否运行
- 验证 `DATABASE_URL` 配置是否正确
- 确保数据库已创建

### API 密钥错误

- 检查 `.env` 文件中的所有 API 密钥
- 确保密钥有效且未过期

### 导入错误

- 确保已安装所有依赖: `pip install -r requirements.txt`
- 检查 Python 版本是否为 3.9+


