# 配置检查清单

使用此清单确保所有配置都已完成。

## 📦 基础环境

- [ ] Python 3.9+ 已安装
- [ ] PostgreSQL 数据库已安装并运行
- [ ] 所有 Python 依赖已安装 (`python -m pip install -r requirements.txt`)

## 🔑 API 密钥配置

### Facebook API
- [ ] `FACEBOOK_APP_ID` - 从 Facebook Developer Console 获取
- [ ] `FACEBOOK_APP_SECRET` - 从 Facebook Developer Console 获取
- [ ] `FACEBOOK_ACCESS_TOKEN` - 长期访问令牌
- [ ] `FACEBOOK_VERIFY_TOKEN` - 自定义的 Webhook 验证令牌（可以是任意字符串）

### OpenAI API
- [ ] `OPENAI_API_KEY` - 从 https://platform.openai.com/api-keys 获取

### Telegram Bot
- [ ] `TELEGRAM_BOT_TOKEN` - 通过 @BotFather 创建 Bot 获取
- [ ] `TELEGRAM_CHAT_ID` - 接收通知的聊天 ID

### 可选集成
- [ ] `MANYCHAT_API_KEY` - 如果使用 ManyChat
- [ ] `BOTCAKE_API_KEY` - 如果使用 Botcake

## 🗄️ 数据库配置

- [ ] PostgreSQL 服务正在运行
- [ ] 已创建数据库：`CREATE DATABASE facebook_customer_service;`
- [ ] `.env` 文件中的 `DATABASE_URL` 已正确配置
  - 格式：`postgresql://用户名:密码@主机:端口/数据库名`
  - 示例：`postgresql://postgres:password@localhost:5432/facebook_customer_service`

## 📝 配置文件

- [ ] `.env` 文件已创建并配置了所有必需的密钥
- [ ] `config.yaml` 文件已创建（已自动从模板复制）
- [ ] `SECRET_KEY` 已设置（可以是随机字符串）

## 🔧 数据库迁移

- [ ] 已运行数据库迁移：`alembic upgrade head`
  - 或者使用：`python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"`

## 🌐 Webhook 配置

### Facebook Webhook
- [ ] Webhook URL 已配置：`https://your-domain.com/webhook`
- [ ] 验证令牌已设置（与 `.env` 中的 `FACEBOOK_VERIFY_TOKEN` 一致）
- [ ] 已订阅事件：`messages`, `messaging_postbacks`, `feed`

### Telegram Webhook（可选）
- [ ] Telegram Bot Webhook 已设置：`https://your-domain.com/telegram/webhook`

## ✅ 验证步骤

运行以下命令验证配置：

```bash
# 1. 测试配置加载
python -c "from src.config import settings; print('配置加载成功！')"

# 2. 测试数据库连接
python -c "from src.database.database import engine; engine.connect(); print('数据库连接成功！')"

# 3. 启动服务
python run.py
```

访问以下 URL 验证服务：
- 健康检查：http://localhost:8000/health
- API 文档：http://localhost:8000/docs

## 🚀 启动服务

配置完成后，运行：

```bash
python run.py
```

或

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📞 获取帮助

如果遇到问题：
1. 查看 `SETUP_INSTRUCTIONS.md` 获取详细说明
2. 查看 `README.md` 了解系统架构
3. 检查日志输出查找错误信息


