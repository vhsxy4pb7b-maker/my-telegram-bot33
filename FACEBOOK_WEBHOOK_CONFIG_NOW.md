# ✅ 在 Facebook 中配置 Webhook - 详细步骤

## 🎯 配置信息

- **回调 URL**: `https://my-telegram-bot33.zeabur.app/webhook`
- **验证令牌**: `J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n`

---

## 📍 第一步：进入 Webhook 设置页面

### 方法 1：直接访问（最快）

在浏览器中访问：
```
https://developers.facebook.com/apps/848496661333193/webhooks/
```

### 方法 2：通过菜单导航

1. 访问：https://developers.facebook.com/
2. 点击 "我的应用" 或 "My Apps"
3. 选择你的应用（App ID: 848496661333193）
4. 左侧菜单 → **产品** → **Messenger** → **设置** → **Webhooks**

---

## ⚙️ 第二步：添加回调 URL

### 2.1 点击添加按钮

1. 在 Webhooks 部分，找到 **"添加回调 URL"** 或 **"Add Callback URL"** 按钮
2. 点击按钮

### 2.2 输入回调 URL

在 "回调 URL" 或 "Callback URL" 输入框中输入：

```
https://my-telegram-bot33.zeabur.app/webhook
```

⚠️ **重要检查：**
- ✅ 以 `https://` 开头（不是 `http://`）
- ✅ 域名后面直接跟 `/webhook`（不要有多余的斜杠）
- ✅ 没有空格

---

## 🔑 第三步：输入验证令牌

### 3.1 找到验证令牌输入框

在同一个对话框中，找到 **"验证令牌"** 或 **"Verify Token"** 输入框

### 3.2 输入验证令牌

1. **完全清空输入框**（如果有默认值）
   - 选中所有文本（Ctrl+A）
   - 删除
   - 确认输入框完全为空

2. **输入验证令牌**：
   ```
   J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n
   ```

3. **检查：**
   - ✅ 没有前后空格
   - ✅ 没有换行符
   - ✅ 与 Zeabur 环境变量中的值完全一致

---

## ✅ 第四步：验证并保存

### 4.1 点击验证按钮

1. 找到 **"验证并保存"** 或 **"Verify and Save"** 按钮
2. 点击按钮

### 4.2 等待验证结果

Facebook 会向你的 Webhook URL 发送验证请求，等待几秒钟。

### 4.3 检查验证结果

**成功：**
- ✅ 显示 **"已验证"** 或 **"Verified"**
- ✅ Webhook 状态变为绿色
- ✅ 回调 URL 旁边显示 ✅ 图标

**失败：**
- ❌ 显示错误信息，例如：
  - "回调 URL 或验证令牌无法验证"
  - "无法连接到服务器"
- 如果失败，参考下面的"故障排查"部分

---

## 📨 第五步：订阅事件

验证成功后，需要订阅事件：

### 5.1 找到订阅字段

1. 在 Webhook 配置下方，找到 **"订阅字段"** 或 **"Subscription Fields"**
2. 或者点击 Webhook 旁边的 **"编辑"** 或 **"Edit"** 按钮

### 5.2 勾选必需事件

在订阅字段列表中，勾选以下事件：

1. ✅ **`messages`** - 接收用户发送的消息（**必须勾选**）
2. ✅ **`messaging_postbacks`** - 接收按钮点击事件（建议勾选）
3. ✅ **`message_deliveries`** - 接收消息送达通知（可选）
4. ✅ **`message_reads`** - 接收消息已读通知（可选）

### 5.3 保存订阅

1. 点击 **"保存更改"** 或 **"Save Changes"** 按钮
2. 确认保存成功

---

## ✅ 第六步：验证配置

### 6.1 检查 Webhook 状态

在 Webhooks 设置页面，确认：

- ✅ 回调 URL 显示为 **"已验证"** 或 **"Verified"**
- ✅ 订阅的事件列表显示已勾选
- ✅ Webhook 状态为 **"活跃"** 或 **"Active"**

### 6.2 测试 Webhook（可选）

1. **在 Facebook 页面发送测试消息**
   - 打开你的 Facebook 页面
   - 发送一条测试消息，例如：`你好`

2. **查看 Zeabur 日志**
   - 在 Zeabur 项目页面 → Logs
   - 应该看到类似日志：
     ```
     收到 Facebook 消息事件
     处理消息: 你好
     ```

3. **检查 AI 回复**
   - 在 Facebook Messenger 中查看
   - 应该收到 AI 自动生成的回复

---

## 🔧 故障排查

### 问题 1：验证失败 - "回调 URL 或验证令牌无法验证"

**可能原因：**
1. 验证令牌不匹配
2. URL 格式错误
3. 应用未运行

**解决步骤：**

1. **检查验证令牌**
   - 在 Zeabur 中重新确认 `FACEBOOK_VERIFY_TOKEN` 的值
   - 在 Facebook 中完全清空输入框，重新粘贴

2. **检查 URL 格式**
   - 确认是：`https://my-telegram-bot33.zeabur.app/webhook`
   - 确认没有多余的空格或斜杠

3. **测试应用可访问性**
   - 访问：`https://my-telegram-bot33.zeabur.app/health`
   - 应该返回：`{"status":"healthy"}`

4. **查看 Zeabur 日志**
   - 检查是否有验证请求的日志
   - 查看是否有错误信息

### 问题 2：收不到消息事件

**可能原因：**
1. 未订阅 `messages` 事件
2. 页面未关联到应用
3. 权限不足

**解决步骤：**

1. **确认已订阅事件**
   - 回到 Webhook 设置页面
   - 确认 `messages` 已勾选

2. **检查页面关联**
   - 在 Messenger 设置中，确认页面已关联到应用

3. **检查权限**
   - 确认应用有 `pages_messaging` 权限

---

## 📋 配置检查清单

完成所有步骤后，确认：

- [ ] ✅ 已进入 Facebook Webhook 设置页面
- [ ] ✅ 已添加回调 URL：`https://my-telegram-bot33.zeabur.app/webhook`
- [ ] ✅ 已输入验证令牌：`J7kP9qR2sT5vW8yZ1bC3dE6fG9hJ2kM4n`
- [ ] ✅ Webhook 验证成功（显示 "已验证"）
- [ ] ✅ 已订阅 `messages` 事件
- [ ] ✅ 已保存所有更改
- [ ] ✅ 测试消息可以正常接收
- [ ] ✅ AI 可以自动回复

---

## 🎉 配置完成！

如果所有检查项都通过，你的 Facebook Webhook 已经配置完成！

**下一步：**
1. ✅ Webhook 已验证
2. ✅ 已订阅必需事件
3. 🧪 发送测试消息到 Facebook 页面
4. 📊 查看实时监控面板
5. 🚀 系统已准备就绪，可以开始使用了！

---

## 📚 相关文档

- [一步步操作指南](./STEP_BY_STEP_WEBHOOK_SETUP.md)
- [Webhook 配置快速参考](./WEBHOOK_CONFIG_QUICK_REFERENCE.md)
- [故障排查指南](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
- [系统配置验证指南](./VERIFY_SYSTEM_SETUP.md)

