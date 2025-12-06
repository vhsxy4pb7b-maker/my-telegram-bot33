# API 测试指南

## 🎉 系统状态

所有 API 测试已通过！系统运行正常。

## 📚 API 文档

API 文档已在浏览器中打开：http://localhost:8000/docs

在 API 文档中，您可以：
- 查看所有可用的 API 端点
- 查看请求和响应的详细格式
- 直接测试各个端点
- 查看示例数据

## 🔍 可用的 API 端点

### 1. 系统信息
- **端点**: `GET /`
- **描述**: 获取系统基本信息
- **测试**: ✅ 通过

**响应示例**:
```json
{
  "message": "Facebook 客服自动化系统",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. 健康检查
- **端点**: `GET /health`
- **描述**: 检查系统健康状态
- **测试**: ✅ 通过

**响应示例**:
```json
{
  "status": "healthy"
}
```

### 3. Facebook Webhook 验证
- **端点**: `GET /webhook`
- **描述**: Facebook Webhook 验证（用于配置 Webhook）
- **测试**: ✅ 通过

**参数**:
- `hub.mode`: `subscribe`
- `hub.verify_token`: 验证令牌（从 .env 读取）
- `hub.challenge`: 挑战字符串

### 4. Facebook Webhook 接收
- **端点**: `POST /webhook`
- **描述**: 接收 Facebook 消息（广告、私信、评论）
- **使用**: 需要在 Facebook Developer Console 中配置

### 5. Telegram Bot 消息处理
- **端点**: `POST /telegram`
- **描述**: 处理 Telegram Bot 消息（审核命令等）

## 🧪 测试方法

### 方法 1: 使用 API 文档（推荐）

1. 在浏览器中打开 http://localhost:8000/docs
2. 展开要测试的端点
3. 点击 "Try it out"
4. 填写参数（如果需要）
5. 点击 "Execute"
6. 查看响应结果

### 方法 2: 使用测试脚本

运行测试脚本：
```bash
python test_api.py
```

### 方法 3: 使用 curl

```bash
# 测试系统信息
curl http://localhost:8000/

# 测试健康检查
curl http://localhost:8000/health

# 测试 Webhook 验证
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test"
```

### 方法 4: 使用 PowerShell

```powershell
# 测试系统信息
Invoke-WebRequest -Uri "http://localhost:8000/" | Select-Object -ExpandProperty Content

# 测试健康检查
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -ExpandProperty Content
```

## 📋 测试清单

- [x] 系统信息端点
- [x] 健康检查端点
- [x] Webhook 验证端点
- [ ] Webhook 接收消息（需要 Facebook 配置）
- [ ] Telegram Bot 消息处理（需要发送消息）

## 🚀 下一步

### 1. 配置 Facebook Webhook（生产环境）

1. 访问 Facebook Developer Console
2. 进入您的应用设置
3. 配置 Webhook URL（需要 HTTPS）
4. 使用验证令牌验证 Webhook

### 2. 测试完整流程

1. 发送测试消息到 Facebook
2. 检查系统是否接收消息
3. 检查 AI 是否生成回复
4. 检查 Telegram 是否收到通知

### 3. 监控系统

- 查看服务日志
- 监控 API 响应时间
- 检查错误日志

## 💡 提示

- API 文档支持交互式测试，非常方便
- 所有端点都有详细的文档说明
- 可以在文档中直接查看请求/响应示例
- 如果遇到问题，检查服务日志

## 🆘 需要帮助？

- 查看 `USAGE_GUIDE.md` 获取使用指南
- 查看 `API_KEYS_GUIDE.md` 获取 API 密钥配置
- 检查服务日志查看错误信息

