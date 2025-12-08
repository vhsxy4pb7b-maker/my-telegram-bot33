# 🔧 修复 "缺少 hub.challenge 参数" 错误

## ❌ 错误信息

```
{"detail":[{"type":"missing","loc":["query","hub.challenge"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.5/v/missing"}]}
```

## 🔍 问题原因

这个错误表示访问 Webhook 端点时，URL 中缺少 `hub.challenge` 参数。

## ✅ 解决方案

### 方法 1：使用完整的测试 URL（推荐）

在浏览器中测试时，必须包含所有三个参数：

```
https://my-telegram-bot33.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n&hub.challenge=test123
```

**参数说明：**
- `hub.mode=subscribe` - 验证模式
- `hub.verify_token=J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n` - 你的验证令牌
- `hub.challenge=test123` - 挑战字符串（可以是任何值）

**预期结果：**
- ✅ 如果返回 `test123`：验证成功！
- ❌ 如果返回 `{"detail":"Verification failed"}`：验证令牌不匹配

---

### 方法 2：在 Facebook 中配置（正确方式）

Facebook 会自动发送所有必需的参数，所以不需要手动测试。

**步骤：**

1. **访问 Webhook 设置页面**
   ```
   https://developers.facebook.com/apps/848496661333193/webhooks/
   ```

2. **添加回调 URL**
   - 点击 "添加回调 URL" 或 "Add Callback URL"
   - 输入：`https://my-telegram-bot33.zeabur.app/webhook`

3. **输入验证令牌**
   - 输入：`J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n`
   - ⚠️ 确保没有多余空格

4. **点击 "验证并保存"**
   - Facebook 会自动发送包含所有参数的验证请求
   - 如果配置正确，会显示 ✅ "已验证"

---

## 🧪 测试步骤

### 1. 测试健康检查

```
https://my-telegram-bot33.zeabur.app/health
```

应该返回：`{"status":"healthy"}`

### 2. 测试 Webhook 验证（使用完整 URL）

```
https://my-telegram-bot33.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n&hub.challenge=test123
```

应该返回：`test123`

### 3. 在 Facebook 中配置

如果步骤 2 返回 `test123`，说明验证端点工作正常，可以在 Facebook 中配置了。

---

## ⚠️ 常见错误

### 错误 1：缺少参数

**错误 URL：**
```
https://my-telegram-bot33.zeabur.app/webhook
```

**正确 URL：**
```
https://my-telegram-bot33.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n&hub.challenge=test123
```

### 错误 2：参数格式错误

**错误：** 参数之间有空格或格式不正确

**正确：** 使用 `&` 连接参数，使用 `=` 连接键值对

---

## 📋 完整测试 URL

复制以下 URL 到浏览器中测试（已包含所有必需参数）：

```
https://my-telegram-bot33.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n&hub.challenge=test123
```

**如果返回 `test123`：**
- ✅ 验证端点工作正常
- ✅ 可以在 Facebook 中配置 Webhook 了

**如果返回错误：**
- 查看具体错误信息
- 检查验证令牌是否正确
- 检查应用是否正在运行

---

## 🎯 下一步

如果测试通过（返回 `test123`）：

1. 在 Facebook 中配置 Webhook
2. 订阅必需事件（`messages` 等）
3. 发送测试消息验证

