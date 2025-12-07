# ✅ 系统配置验证指南

## 📋 验证检查清单

按照以下步骤逐一验证每个检查项：

---

## [ ] 1. Facebook Webhook 已验证

### 验证步骤：

1. **访问 Facebook Webhook 设置**
   - 打开：https://developers.facebook.com/apps/848496661333193/webhooks/
   - 或通过：产品 → Messenger → 设置 → Webhooks

2. **检查 Webhook 状态**
   - 找到你添加的 Webhook
   - 确认显示 **"已验证"** 或 **"Verified"** ✅
   - 如果显示未验证，点击 "验证并保存" 重新验证

3. **验证结果**
   - ✅ 显示 "已验证"：完成
   - ❌ 显示错误：参考 [Webhook 验证故障排查](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)

---

## [ ] 2. 已订阅必需事件

### 验证步骤：

1. **在 Facebook Webhook 设置页面**
   - 找到你的 Webhook
   - 点击 **"订阅字段"** 或 **"Subscription Fields"**

2. **检查已订阅的事件**
   确认以下事件已勾选：
   - ✅ `messages` - 接收用户消息
   - ✅ `messaging_postbacks` - 接收按钮点击
   - ✅ `message_deliveries` - 消息送达通知
   - ✅ `message_reads` - 消息已读通知

3. **如果未订阅**
   - 勾选上述事件
   - 点击 "保存更改"

---

## [ ] 3. 应用正在运行

### 验证步骤：

1. **在 Zeabur 项目页面**
   - 登录 https://zeabur.com
   - 进入你的项目
   - 点击你的应用服务

2. **检查服务状态**
   - 查看服务状态显示
   - ✅ 应该显示 "Running" 或 "运行中"
   - ❌ 如果显示 "Failed" 或 "Error"，查看日志并修复

3. **查看最新日志**
   - 点击 "Logs" 标签
   - 确认看到：`Application startup complete`
   - 确认没有错误信息

---

## [ ] 4. 健康检查通过

### 验证步骤：

1. **获取你的 Zeabur 域名**
   - 在 Zeabur 项目页面找到域名
   - 格式：`your-service.zeabur.app`

2. **测试健康检查端点**
   在浏览器中访问：
   ```
   https://你的域名.zeabur.app/health
   ```

3. **验证结果**
   - ✅ 返回 `{"status": "healthy"}`：通过
   - ❌ 无法访问或返回错误：检查应用是否运行

4. **如果无法访问**
   - 检查服务是否正在运行
   - 查看 Zeabur 日志中的错误
   - 参考 [服务无响应修复指南](./FIX_SERVICE_NOT_RESPONDING.md)

---

## [ ] 5. 测试消息可以正常接收

### 验证步骤：

1. **发送测试消息**
   - 打开你的 Facebook 页面
   - 使用测试账号或真实账号
   - 向页面发送一条消息，例如：`你好`

2. **查看 Zeabur 日志**
   - 在 Zeabur 项目页面 → Logs
   - 应该看到类似日志：
     ```
     收到 Facebook 消息事件
     处理消息: 你好
     ```

3. **验证结果**
   - ✅ 日志中看到消息接收记录：通过
   - ❌ 没有日志记录：检查 Webhook 配置

4. **如果收不到消息**
   - 确认 Webhook 已验证
   - 确认已订阅 `messages` 事件
   - 检查应用是否正在运行
   - 查看 Zeabur 日志中的错误

---

## [ ] 6. AI 可以自动回复

### 验证步骤：

1. **发送测试消息**
   - 在 Facebook 页面发送消息
   - 等待几秒钟

2. **检查是否收到回复**
   - 在 Facebook Messenger 中查看
   - 应该收到 AI 自动生成的回复

3. **查看处理日志**
   - 在 Zeabur Logs 中查找：
     ```
     AI 回复生成成功
     消息已发送到 Facebook
     ```

4. **验证结果**
   - ✅ 收到 AI 回复：通过
   - ❌ 没有回复：检查以下内容

5. **如果 AI 不回复**
   - 检查 `OPENAI_API_KEY` 是否有效
   - 检查 OpenAI API 是否有余额
   - 查看日志中的错误信息
   - 确认 AI 回复功能已启用

---

## [ ] 7. 监控面板可以正常显示

### 验证步骤：

1. **配置监控面板**
   - 打开 `monitoring_dashboard.html` 文件
   - 找到 `API_BASE` 配置（通常在文件开头）
   - 修改为你的 Zeabur 域名：
     ```javascript
     const API_BASE = 'https://你的域名.zeabur.app';
     ```
   - 例如：
     ```javascript
     const API_BASE = 'https://my-telegram-bot33.zeabur.app';
     ```

2. **打开监控面板**
   - 在浏览器中打开 `monitoring_dashboard.html`
   - 或右键文件 → 打开方式 → 浏览器

3. **检查显示内容**
   应该看到：
   - ✅ 实时统计数据（今日回复数、客户数等）
   - ✅ AI 回复列表（如果有回复）
   - ✅ 时间显示正确（本地时区）
   - ✅ "最后更新" 时间在变化

4. **验证结果**
   - ✅ 所有内容正常显示：通过
   - ❌ 显示错误或空白：检查以下内容

5. **如果监控面板无法显示**
   - 确认 `API_BASE` 配置正确
   - 确认应用正在运行
   - 打开浏览器控制台（F12）查看错误
   - 测试 API 端点是否可访问

---

## 🧪 完整测试流程

### 端到端测试

1. **准备**
   - 确认所有环境变量已配置
   - 确认应用正在运行
   - 确认 Webhook 已验证

2. **发送测试消息**
   - 在 Facebook 页面发送：`你好，我想了解 iPhone 贷款`
   - 等待 5-10 秒

3. **验证处理流程**
   - ✅ Facebook 收到 AI 回复
   - ✅ Zeabur 日志显示处理记录
   - ✅ 监控面板显示新的回复记录
   - ✅ 统计数据更新

4. **检查数据**
   - 访问：`https://你的域名.zeabur.app/statistics/ai-replies?limit=5`
   - 应该看到刚才的回复记录

---

## 🔍 快速验证命令

### 使用浏览器测试

1. **健康检查：**
   ```
   https://你的域名.zeabur.app/health
   ```

2. **API 文档：**
   ```
   https://你的域名.zeabur.app/docs
   ```

3. **统计接口：**
   ```
   https://你的域名.zeabur.app/statistics/daily
   ```

### 使用 curl 测试（可选）

```bash
# 健康检查
curl https://你的域名.zeabur.app/health

# 测试 Webhook 端点
curl "https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的令牌&hub.challenge=test123"
```

---

## ⚠️ 常见问题

### 问题 1: Webhook 验证失败

**解决：**
- 参考 [Webhook 验证故障排查](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
- 检查 URL 和验证令牌

### 问题 2: 收不到消息

**解决：**
- 确认 Webhook 已验证
- 确认已订阅 `messages` 事件
- 检查应用是否运行

### 问题 3: AI 不回复

**解决：**
- 检查 `OPENAI_API_KEY` 是否有效
- 检查 OpenAI API 余额
- 查看日志中的错误

### 问题 4: 监控面板无法显示

**解决：**
- 确认 `API_BASE` 配置正确
- 确认应用正在运行
- 检查浏览器控制台错误

---

## 📋 验证完成清单

完成所有验证后，确认：

- [x] Facebook Webhook 已验证
- [x] 已订阅必需事件
- [x] 应用正在运行
- [x] 健康检查通过
- [x] 测试消息可以正常接收
- [x] AI 可以自动回复
- [x] 监控面板可以正常显示

---

## 🎉 验证完成！

如果所有检查项都通过，你的系统已经：

- ✅ 可以接收 Facebook 消息
- ✅ 可以自动生成 AI 回复
- ✅ 可以记录统计数据
- ✅ 可以实时监控运行状态

**系统已准备就绪，可以开始使用了！** 🚀

---

## 📚 相关文档

- [Webhook 配置指南](./FACEBOOK_WEBHOOK_SETUP.md)
- [配置完成后的操作](./AFTER_WEBHOOK_SETUP.md)
- [实时监控指南](./REALTIME_MONITORING_GUIDE.md)
- [故障排查指南](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)

