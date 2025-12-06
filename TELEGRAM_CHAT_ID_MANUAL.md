# 手动获取 Telegram Chat ID

## 方法 1: 通过 API 获取（推荐）

### 步骤 1: 向 Bot 发送消息

1. 打开 Telegram 应用或网页版
2. 找到您的 Bot
3. 向 Bot 发送任意消息（例如：`/start` 或 `hello`）

### 步骤 2: 访问 API

在浏览器中访问以下 URL（替换 `YOUR_BOT_TOKEN` 为您的 Bot Token）：

```
https://api.telegram.org/bot7893216862:AAHkgfAuN4sLrMT3CGIYkTQIPoyjPwixqbw/getUpdates
```

### 步骤 3: 查找 Chat ID

在返回的 JSON 中，查找 `chat` 对象中的 `id` 字段：

```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456789,
      "message": {
        "chat": {
          "id": 123456789,  // 这就是 Chat ID
          "type": "private",
          "first_name": "Your Name"
        }
      }
    }
  ]
}
```

### 步骤 4: 保存到 .env

将找到的 Chat ID 添加到 `.env` 文件：

```
TELEGRAM_BOT_TOKEN=7893216862:AAHkgfAuN4sLrMT3CGIYkTQIPoyjPwixqbw
TELEGRAM_CHAT_ID=你的ChatID
```

## 方法 2: 使用工具（如果网络正常）

如果网络连接正常，可以运行：

```bash
python get_telegram_chat_id_auto.py 7893216862:AAHkgfAuN4sLrMT3CGIYkTQIPoyjPwixqbw
```

## 方法 3: 使用配置工具

运行配置工具，它会引导您完成所有配置：

```bash
python configure_other_keys.py
```

## 提示

- **Chat ID 格式**：
  - 正数：私聊（例如：`123456789`）
  - 负数：群组（例如：`-1001234567890`）

- **如果未找到消息**：
  - 确保已向 Bot 发送消息
  - 确保 Bot Token 正确
  - 等待几秒钟后再尝试

- **网络问题**：
  - 如果遇到连接超时，可以使用方法 1（浏览器访问 API）
  - 或检查网络连接和防火墙设置

## 快速配置

如果已经获取了 Chat ID，可以直接编辑 `.env` 文件添加：

```
TELEGRAM_BOT_TOKEN=7893216862:AAHkgfAuN4sLrMT3CGIYkTQIPoyjPwixqbw
TELEGRAM_CHAT_ID=你的ChatID
```

然后运行验证：

```bash
python verify_setup.py
```

