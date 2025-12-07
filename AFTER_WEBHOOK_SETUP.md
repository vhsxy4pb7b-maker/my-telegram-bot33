# ✅ Facebook Webhook 配置完成后的操作指南

## 🎉 恭喜！Webhook 已配置完成

配置完 Facebook Webhook 后，你的系统已经可以接收和处理消息了。以下是后续操作和验证步骤。

---

## 🧪 第一步：验证 Webhook 配置

### 1. 确认 Webhook 状态

在 Facebook Developers 中：
1. 访问：https://developers.facebook.com/apps/848496661333193/webhooks/
2. 确认 Webhook 显示为 **"已验证"** 或 **"Verified"**
3. 确认已订阅的事件：
   - ✅ `messages`
   - ✅ `messaging_postbacks`
   - ✅ `message_deliveries`
   - ✅ `message_reads`

### 2. 测试 Webhook 连接

在 Facebook Webhook 设置页面：
1. 找到你的 Webhook
2. 点击 **"测试"** 或 **"Test"** 按钮
3. 选择要测试的事件类型
4. 查看 Zeabur 日志，确认收到测试事件

---

## 📱 第二步：测试完整流程

### 1. 发送测试消息

1. **打开你的 Facebook 页面**
   - 使用测试账号或真实账号
   - 向页面发送一条消息

2. **观察系统响应**
   - 系统应该自动回复（使用 AI 生成）
   - 回复内容应该符合你的 AI 提示词设置

### 2. 查看处理日志

在 Zeabur 项目页面 → Logs：

**应该看到：**
```
收到 Facebook 消息事件
AI 回复生成成功
消息已发送到 Facebook
```

**如果看到错误：**
- 检查错误信息
- 根据错误类型修复问题

---

## 📊 第三步：使用监控面板

### 1. 配置监控面板

1. **打开 `monitoring_dashboard.html` 文件**

2. **修改 API 地址：**
   ```javascript
   const API_BASE = 'https://你的域名.zeabur.app';
   ```
   例如：
   ```javascript
   const API_BASE = 'https://my-telegram-bot33.zeabur.app';
   ```

3. **在浏览器中打开文件**
   - 双击文件，或右键 → 打开方式 → 浏览器

### 2. 监控面板功能

监控面板会显示：

- **实时 AI 回复**
  - 最新的 AI 回复记录
  - 客户信息
  - 回复时间（本地时区）

- **统计数据**
  - 今日回复总数
  - 唯一客户数
  - 最近1小时回复数
  - 平台分布

- **自动更新**
  - 每5秒自动刷新统计数据
  - 实时接收新的 AI 回复事件

---

## 🔍 第四步：验证系统功能

### 1. 测试消息接收

发送不同类型的消息测试：

1. **普通消息**
   - 发送：`你好`
   - 预期：AI 自动回复

2. **包含关键词的消息**
   - 发送：`iPhone 12`
   - 预期：AI 识别并推进流程

3. **询问价格**
   - 发送：`多少钱`
   - 预期：AI 回复价格信息

### 2. 检查数据库记录

通过 API 查看数据：

1. **查看 AI 回复记录：**
   ```
   https://你的域名.zeabur.app/statistics/ai-replies?limit=10
   ```

2. **查看每日统计：**
   ```
   https://你的域名.zeabur.app/statistics/daily
   ```

3. **查看高频问题：**
   ```
   https://你的域名.zeabur.app/statistics/frequent-questions
   ```

---

## 📈 第五步：监控和维护

### 1. 日常监控

**每天检查：**
- [ ] Zeabur 服务状态（确保运行中）
- [ ] 查看日志（查找错误）
- [ ] 检查 AI 回复质量
- [ ] 查看统计数据

### 2. 性能监控

**关注指标：**
- AI 回复数量
- 客户数量
- 回复时间
- 错误率

### 3. 日志检查

**定期查看：**
- Zeabur 项目页面 → Logs
- 查找 `ERROR` 或 `WARNING`
- 确认没有持续的错误

---

## 🎯 系统功能说明

### 自动处理流程

1. **接收消息**
   - Facebook 发送 Webhook 到你的应用
   - 系统解析消息类型和内容

2. **AI 自动回复**
   - 使用 OpenAI API 生成智能回复
   - 根据你的提示词规则处理
   - 自动识别用户意图并推进流程

3. **数据记录**
   - 保存对话记录到数据库
   - 记录统计数据
   - 追踪高频问题

4. **实时监控**
   - 通过监控面板查看实时回复
   - 查看统计数据和趋势

### 支持的场景

根据你的 AI 提示词，系统可以：

- ✅ 自动识别 iPhone 型号（11-16）
- ✅ 自动识别贷款金额（3000-15000）
- ✅ 自动推进申请流程
- ✅ 自动引流到 Telegram 群组
- ✅ 回答价格和利息问题
- ✅ 处理犹豫和沉默情况

---

## 🔧 优化建议

### 1. 优化 AI 提示词

如果需要调整 AI 行为：

1. **编辑提示词文件：**
   - `src/ai/prompts/iphone_loan_telegram.py`

2. **修改提示词内容**
   - 根据实际使用情况调整规则
   - 优化回复风格

3. **重新部署**
   - 提交更改
   - Zeabur 会自动重新部署

### 2. 调整监控频率

在 `monitoring_dashboard.html` 中：

```javascript
// 修改统计更新频率（默认5秒）
statsInterval = setInterval(updateStats, 5000);
```

### 3. 配置页面自动回复

如果需要为不同页面设置不同的自动回复：

1. **使用配置工具：**
   ```bash
   python configure_page_auto_reply.py
   ```

2. **或通过 API：**
   ```
   POST /facebook/pages/{page_id}/auto-reply
   ```

---

## 📚 相关 API 端点

### 系统端点

- `GET /` - 系统信息
- `GET /health` - 健康检查
- `GET /docs` - API 文档

### 统计端点

- `GET /statistics/daily` - 每日统计
- `GET /statistics/ai-replies` - AI 回复记录
- `GET /statistics/frequent-questions` - 高频问题
- `GET /statistics/summary` - 统计摘要

### 监控端点

- `GET /monitoring/live` - 实时监控流（SSE）
- `GET /monitoring/stats` - 实时统计数据
- `GET /monitoring/recent-replies` - 最近回复

### Facebook Webhook

- `GET /webhook` - Webhook 验证
- `POST /webhook` - 接收 Facebook 事件

---

## ⚠️ 常见问题

### 问题 1: 收不到消息

**检查：**
- Webhook 是否已验证
- 是否订阅了 `messages` 事件
- 应用是否正在运行
- 查看 Zeabur 日志

### 问题 2: AI 不回复

**检查：**
- `OPENAI_API_KEY` 是否有效
- OpenAI API 是否有余额
- 查看日志中的错误信息

### 问题 3: 回复内容不符合预期

**解决：**
- 调整 AI 提示词
- 检查提示词文件是否正确加载
- 查看日志中的提示词内容

---

## 🎓 下一步学习

### 1. 了解系统架构

- 查看 `README.md` 了解系统架构
- 查看代码结构了解实现细节

### 2. 自定义功能

- 修改 AI 提示词
- 添加新的处理逻辑
- 自定义统计指标

### 3. 扩展功能

- 添加更多平台支持
- 集成更多第三方服务
- 优化用户体验

---

## 📞 获取帮助

如果遇到问题：

1. **查看相关文档：**
   - [Webhook 配置指南](./FACEBOOK_WEBHOOK_SETUP.md)
   - [故障排查指南](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
   - [实时监控指南](./REALTIME_MONITORING_GUIDE.md)

2. **检查日志：**
   - Zeabur 项目页面 → Logs
   - 查找错误信息

3. **测试端点：**
   - 使用浏览器测试 API 端点
   - 使用 curl 测试 Webhook

---

## ✅ 完成检查清单

配置完成后，确认以下所有项目：

- [ ] Facebook Webhook 已验证
- [ ] 已订阅必需事件
- [ ] 应用正在运行
- [ ] 健康检查通过
- [ ] 测试消息可以正常接收
- [ ] AI 可以自动回复
- [ ] 监控面板可以正常显示
- [ ] 统计数据可以正常查看

---

**🎉 恭喜！你的系统已经配置完成并可以开始工作了！**

现在可以：
- 接收 Facebook 消息
- 自动生成 AI 回复
- 监控系统运行状态
- 查看统计数据

祝使用愉快！🚀

