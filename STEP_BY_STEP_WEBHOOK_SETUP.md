# 📝 Facebook Webhook 配置 - 一步步操作指南

## 🎯 目标
配置 Facebook Webhook，让 Facebook 能够向你的应用发送消息。

---

## 📋 准备工作

在开始之前，你需要准备：
1. ✅ Zeabur 应用已部署并运行
2. ✅ 知道你的 Zeabur 域名
3. ✅ 知道你的验证令牌（从 Zeabur 环境变量获取）

---

## 🔍 第一步：获取 Zeabur 域名和验证令牌

### 步骤 1.1：登录 Zeabur

1. **打开浏览器**
2. **访问 Zeabur**：https://zeabur.com
3. **登录你的账号**

### 步骤 1.2：找到你的应用服务

1. **进入你的项目**
   - 在 Zeabur 首页，点击你的项目
   - 或直接访问项目页面

2. **找到你的应用服务**
   - 在项目页面中，找到你的应用服务（例如：`my-telegram-bot33`）
   - 点击进入服务详情页

### 步骤 1.3：获取域名

1. **查看服务详情页**
   - 在服务详情页的顶部或侧边栏
   - 找到 **"域名"** 或 **"Domain"** 部分

2. **复制域名**
   - 你会看到类似：`my-telegram-bot33.zeabur.app`
   - **完整复制**这个域名（包括 `.zeabur.app`）
   - 例如：`my-telegram-bot33.zeabur.app`

3. **记录域名**
   - 在记事本或文本编辑器中记录：
     ```
     域名：my-telegram-bot33.zeabur.app
     ```

### 步骤 1.4：获取验证令牌

1. **进入环境变量页面**
   - 在服务详情页，点击 **"Variables"** 或 **"环境变量"** 标签
   - 或点击 **"设置"** → **"环境变量"**

2. **找到验证令牌**
   - 在环境变量列表中，找到 `FACEBOOK_VERIFY_TOKEN`
   - 点击 **"显示"** 或 **"Show"** 按钮（如果有）
   - **完整复制**这个值

3. **记录验证令牌**
   - 在记事本中记录：
     ```
     验证令牌：[你复制的值]
     ```
   - ⚠️ **重要**：
     - 不要有多余的空格
     - 不要有换行符
     - 完整复制所有字符

### 步骤 1.5：验证应用运行状态

1. **测试健康检查**
   - 在浏览器中访问：
     ```
     https://你的域名.zeabur.app/health
     ```
   - 例如：`https://my-telegram-bot33.zeabur.app/health`
   - 应该返回：`{"status": "healthy"}`

2. **如果无法访问**
   - 检查服务状态是否为 "Running"
   - 查看日志是否有错误
   - 等待几分钟后重试

---

## 🌐 第二步：进入 Facebook Webhook 设置页面

### 步骤 2.1：访问 Facebook Developers

1. **打开新标签页**
   - 在浏览器中打开新标签页（保持 Zeabur 页面打开）

2. **访问 Facebook Developers**
   - 在地址栏输入：`https://developers.facebook.com/`
   - 按 Enter 键

3. **登录账号**
   - 如果未登录，使用你的 Facebook 账号登录

### 步骤 2.2：选择你的应用

1. **找到应用列表**
   - 在页面顶部，点击 **"我的应用"** 或 **"My Apps"**
   - 或直接访问：`https://developers.facebook.com/apps/`

2. **选择应用**
   - 在应用列表中找到你的应用
   - 应用 ID 是：`848496661333193`
   - 点击应用名称进入

   **或者直接访问：**
   ```
   https://developers.facebook.com/apps/848496661333193/
   ```

### 步骤 2.3：进入 Webhooks 设置

**方法 1：通过左侧菜单（推荐）**

1. **找到左侧菜单**
   - 在应用页面左侧，找到菜单栏

2. **找到 "产品" 部分**
   - 向下滚动左侧菜单
   - 找到 **"产品"** 或 **"Products"** 部分

3. **点击 "Messenger"**
   - 在 "产品" 部分中，找到 **"Messenger"**
   - 点击进入

4. **进入 "设置"**
   - 在 Messenger 页面中，点击左侧的 **"设置"** 或 **"Settings"**
   - 或点击顶部的 **"设置"** 标签

5. **找到 "Webhooks"**
   - 在设置页面中，向下滚动
   - 找到 **"Webhooks"** 部分

**方法 2：直接访问（最快）**

在浏览器地址栏输入并访问：
```
https://developers.facebook.com/apps/848496661333193/webhooks/
```

按 Enter 键，直接进入 Webhooks 设置页面。

---

## ⚙️ 第三步：配置 Webhook

### 步骤 3.1：添加回调 URL

1. **找到 "添加回调 URL" 按钮**
   - 在 Webhooks 部分，找到 **"添加回调 URL"** 或 **"Add Callback URL"** 按钮
   - 点击按钮

2. **输入回调 URL**
   - 会弹出一个对话框或展开一个表单
   - 找到 **"回调 URL"** 或 **"Callback URL"** 输入框
   - 输入以下格式（替换为你的域名）：
     ```
     https://你的域名.zeabur.app/webhook
     ```
   - **示例**（如果你的域名是 `my-telegram-bot33.zeabur.app`）：
     ```
     https://my-telegram-bot33.zeabur.app/webhook
     ```
   - ⚠️ **重要检查**：
     - ✅ 必须以 `https://` 开头（不是 `http://`）
     - ✅ 域名后面直接跟 `/webhook`（不要有多余的斜杠）
     - ✅ 不要有空格

3. **检查 URL 格式**
   - 正确的格式：`https://域名.zeabur.app/webhook`
   - 错误的格式：
     - ❌ `http://域名.zeabur.app/webhook` （缺少 `s`）
     - ❌ `https://域名.zeabur.app/webhook/` （末尾多了斜杠）
     - ❌ `https://域名.zeabur.app` （缺少 `/webhook`）

### 步骤 3.2：输入验证令牌

1. **找到验证令牌输入框**
   - 在同一个对话框中，找到 **"验证令牌"** 或 **"Verify Token"** 输入框

2. **输入验证令牌**
   - **完全清空**输入框（如果有默认值）
   - 从你之前记录的验证令牌中复制
   - 粘贴到输入框
   - ⚠️ **重要**：
     - 不能有多余的空格（前后都不能有）
     - 不能有换行符
     - 必须与 Zeabur 中的值 **完全一致**

3. **再次确认**
   - 检查输入的值是否与 Zeabur 环境变量中的值完全一致
   - 可以回到 Zeabur 页面对比确认

### 步骤 3.3：验证并保存

1. **点击验证按钮**
   - 找到 **"验证并保存"** 或 **"Verify and Save"** 按钮
   - 点击按钮

2. **等待验证结果**
   - Facebook 会向你的 Webhook URL 发送验证请求
   - 等待几秒钟

3. **检查验证结果**
   - ✅ **成功**：会显示 **"已验证"** 或 **"Verified"**，并且 Webhook 状态变为绿色
   - ❌ **失败**：会显示错误信息，例如：
     - "回调 URL 或验证令牌无法验证"
     - "无法连接到服务器"
     - "验证失败"

4. **如果验证失败**
   - 参考下面的"故障排查"部分
   - 或查看 [Webhook 验证故障排查指南](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)

---

## 📨 第四步：订阅事件

### 步骤 4.1：找到订阅字段

验证成功后，需要订阅事件：

1. **找到 "订阅字段"**
   - 在 Webhook 配置下方，找到 **"订阅字段"** 或 **"Subscription Fields"**
   - 或者点击 Webhook 旁边的 **"编辑"** 或 **"Edit"** 按钮

2. **打开订阅设置**
   - 点击进入订阅字段设置页面

### 步骤 4.2：勾选必需事件

在订阅字段列表中，勾选以下事件：

1. ✅ **`messages`**
   - 说明：接收用户发送的消息
   - **必须勾选**（这是最重要的）

2. ✅ **`messaging_postbacks`**
   - 说明：接收按钮点击事件
   - **建议勾选**

3. ✅ **`message_deliveries`**
   - 说明：接收消息送达通知
   - **可选勾选**

4. ✅ **`message_reads`**
   - 说明：接收消息已读通知
   - **可选勾选**

### 步骤 4.3：保存订阅

1. **点击保存**
   - 找到 **"保存更改"** 或 **"Save Changes"** 按钮
   - 点击保存

2. **确认保存成功**
   - 页面会显示保存成功的提示
   - 订阅的事件列表会显示已勾选

---

## ✅ 第五步：验证配置

### 步骤 5.1：检查 Webhook 状态

在 Webhooks 设置页面，确认：

1. ✅ **回调 URL 状态**
   - 显示为 **"已验证"** 或 **"Verified"**
   - 状态图标为绿色 ✅

2. ✅ **订阅事件**
   - 显示已勾选的事件列表
   - 至少包含 `messages`

3. ✅ **Webhook 状态**
   - 显示为 **"活跃"** 或 **"Active"**

### 步骤 5.2：测试 Webhook（可选）

1. **使用 Facebook 测试工具**
   - 在 Webhook 设置页面，找到 **"测试"** 或 **"Test"** 按钮
   - 点击发送测试事件
   - 检查 Zeabur 日志，确认收到事件

2. **发送测试消息**
   - 在你的 Facebook 页面发送一条测试消息
   - 例如：`你好`
   - 等待几秒钟

3. **检查 Zeabur 日志**
   - 回到 Zeabur 项目页面
   - 点击 **"Logs"** 或 **"日志"** 标签
   - 应该看到类似日志：
     ```
     收到 Facebook 消息事件
     处理消息: 你好
     ```

4. **检查 AI 回复**
   - 在 Facebook Messenger 中查看
   - 应该收到 AI 自动生成的回复

---

## 🔧 故障排查

### 问题 1：验证失败 - "回调 URL 或验证令牌无法验证"

**可能原因：**
1. URL 格式错误
2. 应用未运行
3. 验证令牌不匹配

**解决步骤：**

1. **检查 URL 格式**
   - 确认 URL 是：`https://你的域名.zeabur.app/webhook`
   - 确认没有多余的空格或斜杠

2. **测试 URL 可访问性**
   - 在浏览器中访问：`https://你的域名.zeabur.app/health`
   - 应该返回：`{"status": "healthy"}`
   - 如果无法访问，检查应用是否运行

3. **手动测试 Webhook 端点**
   - 在浏览器中访问（替换为你的实际值）：
     ```
     https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123
     ```
   - 应该返回：`test123`（纯文本）
   - 如果返回错误，说明验证令牌不匹配

4. **重新检查验证令牌**
   - 回到 Zeabur，重新复制 `FACEBOOK_VERIFY_TOKEN`
   - 在 Facebook 中完全清空输入框，重新粘贴
   - 确保没有多余的空格

### 问题 2：无法访问 Webhook URL

**可能原因：**
1. 应用未运行
2. 域名错误
3. DNS 未生效

**解决步骤：**

1. **检查应用状态**
   - 在 Zeabur 中查看服务状态
   - 确认显示 "Running"

2. **检查日志**
   - 查看 Zeabur 日志
   - 确认没有错误信息
   - 应该看到：`Application startup complete`

3. **等待 DNS 生效**
   - 如果是新部署，等待 1-2 分钟
   - 然后重试

### 问题 3：收不到消息事件

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

完成所有步骤后，确认以下所有项：

- [ ] ✅ 已获取 Zeabur 域名
- [ ] ✅ 已获取验证令牌
- [ ] ✅ 应用健康检查通过（`/health` 返回正常）
- [ ] ✅ 已进入 Facebook Webhooks 设置页面
- [ ] ✅ 已添加回调 URL（格式正确）
- [ ] ✅ 已输入验证令牌（与 Zeabur 完全一致）
- [ ] ✅ Webhook 验证成功（显示 "已验证"）
- [ ] ✅ 已订阅 `messages` 事件
- [ ] ✅ 已保存所有更改
- [ ] ✅ 测试消息可以正常接收
- [ ] ✅ AI 可以自动回复

---

## 🎉 配置完成！

如果所有检查项都通过，你的 Facebook Webhook 已经配置完成！

**下一步：**
- 测试发送消息，确认 AI 可以自动回复
- 查看实时监控面板，确认系统正常运行
- 参考 [系统配置验证指南](./VERIFY_SYSTEM_SETUP.md) 进行完整验证

---

## 📚 相关文档

- [Webhook 配置详细指南](./FACEBOOK_WEBHOOK_SETUP.md)
- [Webhook 验证故障排查](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
- [系统配置验证指南](./VERIFY_SYSTEM_SETUP.md)
- [下一步操作指南](./NEXT_STEPS.md)

---

**需要帮助？**
如果遇到问题，请：
1. 查看故障排查部分
2. 查看相关文档
3. 检查 Zeabur 日志
4. 检查 Facebook 开发者控制台的错误信息

