# 快速配置 API 密钥指南

## 当前状态

您的 `.env` 文件已准备好，只需要将占位符替换为真实的 API 密钥。

## 配置方法

### 方法 1：使用配置工具（推荐）

```bash
python configure_api_keys.py
```

工具会引导您一步步输入所有 API 密钥。

### 方法 2：手动编辑 .env 文件

直接打开 `.env` 文件，替换以下占位符：

```env
# Facebook API（必需）
FACEBOOK_APP_ID=your_facebook_app_id          # 替换为实际值
FACEBOOK_APP_SECRET=your_facebook_app_secret  # 替换为实际值
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token  # 替换为实际值
FACEBOOK_VERIFY_TOKEN=your_webhook_verify_token   # 替换为实际值（可自定义）

# OpenAI API（必需）
OPENAI_API_KEY=your_openai_api_key            # 替换为实际值

# Telegram Bot（必需）
TELEGRAM_BOT_TOKEN=your_telegram_bot_token   # 替换为实际值
TELEGRAM_CHAT_ID=your_telegram_chat_id       # 替换为实际值
```

## 获取 API 密钥的快速链接

### Facebook API
1. 访问：https://developers.facebook.com/
2. 创建应用 → 获取 App ID 和 App Secret
3. 生成访问令牌
4. **详细步骤**：查看 `API_KEYS_GUIDE.md` 第 1 节

### OpenAI API
1. 访问：https://platform.openai.com/api-keys
2. 创建新的 API 密钥
3. **详细步骤**：查看 `API_KEYS_GUIDE.md` 第 2 节

### Telegram Bot
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot` 创建 Bot
3. 获取 Chat ID（参考指南）
4. **详细步骤**：查看 `API_KEYS_GUIDE.md` 第 3 节

## 配置优先级

### 必需配置（系统核心功能）
1. ✅ **数据库** - 已完成（使用 SQLite）
2. ⚠️ **Facebook API** - 需要配置（接收消息）
3. ⚠️ **OpenAI API** - 需要配置（AI 回复）
4. ⚠️ **Telegram Bot** - 需要配置（审核通知）

### 可选配置
- ManyChat API（如果使用 ManyChat）
- Botcake API（如果使用 Botcake）

## 配置后验证

配置完成后，运行验证：

```bash
python verify_setup.py
```

## 测试模式

如果暂时没有 API 密钥，系统仍然可以启动，但以下功能将不可用：
- ❌ 接收 Facebook 消息
- ❌ AI 自动回复
- ❌ Telegram 通知

但可以：
- ✅ 查看 API 文档
- ✅ 测试数据库连接
- ✅ 查看系统架构

## 快速开始（最小配置）

如果只想快速测试系统，可以：

1. **只配置 OpenAI API**（用于测试 AI 功能）
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **启动服务**
   ```bash
   python run.py
   ```

3. **访问 API 文档**
   - http://localhost:8000/docs

## 下一步

1. **获取 API 密钥** - 参考 `API_KEYS_GUIDE.md`
2. **配置密钥** - 使用 `python configure_api_keys.py` 或手动编辑 `.env`
3. **验证配置** - 运行 `python verify_setup.py`
4. **启动服务** - 运行 `python run.py`

