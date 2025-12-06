# API 密钥获取指南

本指南帮助您获取系统所需的所有 API 密钥。

## 1. Facebook API 密钥

### 步骤：

1. **访问 Facebook Developers**
   - 网址：https://developers.facebook.com/
   - 使用您的 Facebook 账号登录

2. **创建应用**
   - 点击"我的应用" → "创建应用"
   - 选择"业务"类型
   - 填写应用名称和联系邮箱

3. **获取 App ID 和 App Secret**
   - 在应用仪表板中，找到"设置" → "基本"
   - 复制"应用编号"（App ID）
   - 复制"应用密钥"（App Secret）

4. **生成访问令牌**
   - 在"工具" → "Graph API 资源管理器"中
   - 选择您的应用
   - 点击"生成访问令牌"
   - 选择所需权限（`pages_messaging`, `pages_read_engagement` 等）
   - 复制生成的访问令牌

5. **设置 Webhook 验证令牌**
   - 这是您自定义的字符串，用于验证 Facebook Webhook
   - 可以是任意字符串，例如：`my_secure_verify_token_2024`

### 配置到 .env：
```
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_ACCESS_TOKEN=your_access_token_here
FACEBOOK_VERIFY_TOKEN=your_custom_verify_token
```

---

## 2. OpenAI API 密钥

### 步骤：

1. **访问 OpenAI Platform**
   - 网址：https://platform.openai.com/
   - 登录或注册账号

2. **创建 API 密钥**
   - 点击右上角头像 → "API keys"
   - 点击"Create new secret key"
   - 复制生成的密钥（只显示一次，请妥善保存）

3. **充值账户**（如需要）
   - 确保账户有足够的余额使用 API

### 配置到 .env：
```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

---

## 3. Telegram Bot Token

### 步骤：

1. **创建 Bot**
   - 在 Telegram 中搜索 `@BotFather`
   - 发送 `/newbot` 命令
   - 按照提示设置 Bot 名称和用户名
   - 复制返回的 Bot Token

2. **获取 Chat ID**
   - 方法 1：将 Bot 添加到群组，发送消息，然后访问：
     ```
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```
     在返回的 JSON 中找到 `chat.id`

   - 方法 2：使用 `@userinfobot` 获取个人 Chat ID
   - 方法 3：在代码中临时添加日志输出 Chat ID

### 配置到 .env：
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## 4. ManyChat API 密钥（可选）

### 步骤：

1. **登录 ManyChat**
   - 网址：https://manychat.com/
   - 登录您的账号

2. **获取 API 密钥**
   - 进入"设置" → "API"
   - 生成新的 API 密钥
   - 复制密钥

### 配置到 .env：
```
MANYCHAT_API_KEY=your_manychat_key_here
MANYCHAT_API_URL=https://api.manychat.com
```

---

## 5. Botcake API 密钥（可选）

### 步骤：

1. **登录 Botcake**
   - 网址：https://botcake.com/
   - 登录您的账号

2. **获取 API 密钥**
   - 进入"设置" → "API"
   - 生成新的 API 密钥
   - 复制密钥

### 配置到 .env：
```
BOTCAKE_API_KEY=your_botcake_key_here
BOTCAKE_API_URL=https://api.botcake.com
```

---

## 6. SECRET_KEY（安全密钥）

这是用于应用内部加密的密钥，可以是任意随机字符串。

### 生成方法：

**方法 1：使用 Python**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**方法 2：使用在线工具**
- 访问：https://randomkeygen.com/
- 选择一个随机字符串

### 配置到 .env：
```
SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
```

---

## 安全提示

⚠️ **重要安全建议：**

1. **永远不要**将 `.env` 文件提交到 Git 仓库
2. **永远不要**在公共场合分享您的 API 密钥
3. 定期轮换 API 密钥
4. 为不同的环境使用不同的密钥
5. 使用环境变量或密钥管理服务存储生产环境的密钥

---

## 验证配置

配置完成后，可以使用以下命令验证：

```bash
# 测试配置加载
python -c "from src.config import settings; print('所有配置已加载')"
```

如果出现错误，请检查：
- `.env` 文件是否存在
- 所有必需的密钥是否都已填写
- 密钥格式是否正确（没有多余的空格或引号）


