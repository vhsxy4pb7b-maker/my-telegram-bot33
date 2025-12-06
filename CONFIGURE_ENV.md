# 配置 .env 文件指南

## 当前状态

您的 `.env` 文件已创建，但包含的是默认占位符值。需要替换为真实的 API 密钥和配置。

## 配置步骤

### 1. 打开 .env 文件

使用文本编辑器打开项目根目录下的 `.env` 文件。

### 2. 必需配置项

#### 数据库配置
```
DATABASE_URL=postgresql://用户名:密码@localhost:5432/facebook_customer_service
```
**示例：**
```
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/facebook_customer_service
```

#### Facebook API 配置
需要从 Facebook Developer Console 获取：
- `FACEBOOK_APP_ID`: 应用 ID
- `FACEBOOK_APP_SECRET`: 应用密钥
- `FACEBOOK_ACCESS_TOKEN`: 访问令牌
- `FACEBOOK_VERIFY_TOKEN`: Webhook 验证令牌（可自定义，如：`my_secure_token_2024`）

#### OpenAI API 配置
- `OPENAI_API_KEY`: 从 https://platform.openai.com/api-keys 获取

#### Telegram Bot 配置
- `TELEGRAM_BOT_TOKEN`: 通过 @BotFather 创建 Bot 获取
- `TELEGRAM_CHAT_ID`: 接收通知的聊天 ID

#### 安全密钥
- `SECRET_KEY`: 随机字符串（用于加密），可以使用：
  ```python
  import secrets
  print(secrets.token_urlsafe(32))
  ```

### 3. 可选配置

如果使用 ManyChat 或 Botcake：
- `MANYCHAT_API_KEY`: ManyChat API 密钥
- `BOTCAKE_API_KEY`: Botcake API 密钥

## 配置示例

```env
# 数据库
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/facebook_customer_service
DATABASE_ECHO=false

# Facebook
FACEBOOK_APP_ID=1234567890123456
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_ACCESS_TOKEN=your_long_lived_access_token
FACEBOOK_VERIFY_TOKEN=my_webhook_verify_token_2024

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890

# 安全
SECRET_KEY=your_random_secret_key_here_min_32_chars
ALGORITHM=HS256
```

## 验证配置

配置完成后，运行：
```bash
python verify_setup.py
```

检查环境变量是否正确加载。

## 注意事项

⚠️ **安全提示：**
- 永远不要将 `.env` 文件提交到 Git
- 不要在公共场合分享 API 密钥
- 定期轮换密钥
- 为不同环境使用不同的密钥

