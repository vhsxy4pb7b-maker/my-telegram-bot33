# 完整测试指南

## 📋 测试清单

### 1. ✅ API 文档测试
- [x] 系统信息端点
- [x] 健康检查端点
- [x] Webhook 验证端点
- [ ] 在 API 文档中交互式测试

### 2. ⏳ Facebook Webhook 配置
- [ ] 配置 Webhook URL
- [ ] 验证 Webhook
- [ ] 测试消息接收

### 3. ⏳ 完整流程测试
- [ ] 发送测试消息
- [ ] AI 自动回复
- [ ] Telegram 通知

## 🔍 1. 在 API 文档中测试端点

### 访问 API 文档

打开浏览器访问：http://localhost:8000/docs

### 测试步骤

#### 测试系统信息端点

1. 找到 `GET /` 端点
2. 点击展开
3. 点击 "Try it out"
4. 点击 "Execute"
5. 查看响应结果

**预期响应**:
```json
{
  "message": "Facebook 客服自动化系统",
  "version": "1.0.0",
  "status": "running"
}
```

#### 测试健康检查端点

1. 找到 `GET /health` 端点
2. 点击展开
3. 点击 "Try it out"
4. 点击 "Execute"
5. 查看响应结果

**预期响应**:
```json
{
  "status": "healthy"
}
```

#### 测试 Webhook 验证端点

1. 找到 `GET /webhook` 端点
2. 点击展开
3. 点击 "Try it out"
4. 填写参数：
   - `hub.mode`: `subscribe`
   - `hub.verify_token`: 从 .env 文件中的 `FACEBOOK_VERIFY_TOKEN`
   - `hub.challenge`: `test_challenge_123`
5. 点击 "Execute"
6. 查看响应结果

**预期响应**: 返回 `test_challenge_123`

## 🔧 2. 配置 Facebook Webhook

### 本地测试（开发环境）

对于本地开发，可以使用 ngrok 等工具创建 HTTPS 隧道。

#### 使用 ngrok（推荐）

1. **安装 ngrok**
   - 访问：https://ngrok.com/
   - 下载并安装
   - 注册账号获取 authtoken

2. **启动隧道**
   ```bash
   ngrok http 8000
   ```

3. **获取 HTTPS URL**
   - ngrok 会显示类似：`https://xxxx-xx-xx-xx-xx.ngrok.io`
   - 使用这个 URL 配置 Webhook

4. **配置 Facebook Webhook**
   - Webhook URL: `https://xxxx-xx-xx-xx-xx.ngrok.io/webhook`
   - 验证令牌: 从 .env 文件中的 `FACEBOOK_VERIFY_TOKEN`

### 生产环境配置

1. **访问 Facebook Developer Console**
   - 网址：https://developers.facebook.com/
   - 选择您的应用

2. **配置 Webhook**
   - 进入 "Webhooks" 设置
   - 点击 "Add Callback URL"
   - 输入您的 HTTPS URL（例如：`https://yourdomain.com/webhook`）
   - 输入验证令牌（从 .env 文件中的 `FACEBOOK_VERIFY_TOKEN`）

3. **订阅事件**
   - 选择要订阅的事件：
     - `messages` - 接收消息
     - `messaging_postbacks` - 接收回传
     - `messaging_optins` - 接收选择加入

4. **验证 Webhook**
   - Facebook 会发送验证请求
   - 如果配置正确，会显示 "Verified"

## 🧪 3. 测试完整流程

### 测试脚本

运行完整流程测试脚本：

```bash
python test_complete_flow.py
```

### 手动测试步骤

#### 步骤 1: 发送测试消息到 Facebook

1. 在 Facebook 中向您的页面发送消息
2. 或使用 Facebook Graph API 发送测试消息

#### 步骤 2: 检查系统接收

1. 查看服务日志
2. 检查数据库中的消息记录
3. 验证消息是否被正确解析

#### 步骤 3: 检查 AI 回复

1. 检查 AI 是否生成了回复
2. 查看回复内容
3. 验证回复是否发送回 Facebook

#### 步骤 4: 检查 Telegram 通知

1. 检查 Telegram 是否收到通知
2. 验证通知内容
3. 测试审核命令（如果适用）

## 📝 测试脚本说明

### test_complete_flow.py

这个脚本会：
1. 模拟 Facebook Webhook 消息
2. 测试消息处理流程
3. 检查 AI 回复生成
4. 验证 Telegram 通知

### 运行测试

```bash
python test_complete_flow.py
```

## ⚠️ 注意事项

### 本地测试限制

- Facebook Webhook 需要 HTTPS
- 本地开发需要使用 ngrok 等工具
- 生产环境需要配置真实的 HTTPS 域名

### 测试数据

- 使用测试数据，不要使用真实客户数据
- 确保测试不会影响生产环境
- 测试完成后清理测试数据

### 错误处理

- 检查服务日志查看错误信息
- 验证所有 API 密钥是否正确
- 确保数据库连接正常

## 🆘 常见问题

### 问题 1: Webhook 验证失败

**原因**: 验证令牌不匹配

**解决**: 
- 检查 .env 文件中的 `FACEBOOK_VERIFY_TOKEN`
- 确保 Facebook 中配置的令牌相同

### 问题 2: 消息未接收

**原因**: Webhook 未正确配置

**解决**:
- 检查 Webhook URL 是否正确
- 确保已订阅相应的事件
- 检查服务是否运行

### 问题 3: AI 未回复

**原因**: OpenAI API 配置问题

**解决**:
- 检查 OpenAI API Key 是否正确
- 确保账户有足够余额
- 查看错误日志

## 📚 相关文档

- **API_TESTING_GUIDE.md** - API 测试详细指南
- **USAGE_GUIDE.md** - 系统使用指南
- **API_KEYS_GUIDE.md** - API 密钥配置指南

