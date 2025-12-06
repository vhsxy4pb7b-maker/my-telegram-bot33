# 获取 Facebook 访问令牌 - 完整流程

## ✅ 当前状态

授权 URL 已正常工作！现在可以看到 Facebook 登录页面。

## 📋 获取访问令牌的步骤

### 步骤 1: 登录 Facebook

1. 在授权 URL 页面中，输入您的 Facebook 账号和密码
2. 点击"登录"

### 步骤 2: 授权应用权限

登录后，您会看到授权页面，显示应用请求的权限：
- ✅ pages_messaging - 发送和接收消息
- ✅ pages_read_engagement - 读取页面互动数据
- ✅ pages_manage_metadata - 管理页面元数据

点击"继续"或"授权"按钮。

### 步骤 3: 获取访问令牌

授权成功后，浏览器会重定向到：

```
http://localhost:8000/oauth/callback#access_token=YOUR_ACCESS_TOKEN&token_type=bearer&expires_in=5183944
```

**重要**: 从 URL 的 `#` 后面提取 `access_token` 的值。

### 步骤 4: 提取访问令牌

有两种方式：

#### 方法 1: 使用提取工具（推荐）

复制完整的重定向 URL，然后运行：

```bash
python extract_token.py "完整的重定向URL"
```

#### 方法 2: 手动提取

从 URL 中找到 `access_token=` 后面的值（到 `&` 之前）。

例如，如果 URL 是：
```
http://localhost:8000/oauth/callback#access_token=EAABwzLix...&token_type=bearer&expires_in=5183944
```

那么访问令牌就是：`EAABwzLix...`（整个值，直到 `&` 之前）

### 步骤 5: 配置到系统

获取访问令牌后：

```bash
python configure_api_keys.py
```

或手动编辑 `.env` 文件：
```env
FACEBOOK_ACCESS_TOKEN=你的访问令牌
```

### 步骤 6: 交换长期令牌（可选但推荐）

默认获取的是短期令牌（1-2小时）。要获取长期令牌（60天）：

```bash
python exchange_token.py
```

需要提供：
- 短期访问令牌
- App ID: 848496661333193
- App Secret（从 Facebook Developer Console 获取）

## ⚠️ 注意事项

1. **访问令牌是敏感信息**
   - 不要分享给他人
   - 不要提交到 Git
   - 妥善保管

2. **令牌有效期**
   - 短期令牌：1-2 小时
   - 长期令牌：60 天
   - 建议使用长期令牌

3. **如果授权失败**
   - 检查应用是否已通过 Facebook 审核（某些权限需要）
   - 确认已配置所有必需的设置
   - 检查浏览器控制台是否有错误

## 🔄 完整流程总结

1. ✅ 配置应用域名 - 已完成
2. ✅ 访问授权 URL - 当前步骤
3. ⏳ 登录并授权 - 进行中
4. ⏳ 获取访问令牌 - 下一步
5. ⏳ 配置到系统 - 待完成
6. ⏳ 交换长期令牌 - 可选

## 📝 快速命令参考

```bash
# 提取令牌
python extract_token.py "重定向URL"

# 配置到系统
python configure_api_keys.py

# 交换长期令牌
python exchange_token.py

# 验证配置
python verify_setup.py
```

## 🎯 下一步

完成授权后，您将获得访问令牌，然后可以：
1. 配置到系统
2. 测试 Facebook API 连接
3. 配置 Webhook 开始接收消息
4. 开始使用完整的系统功能

祝您配置顺利！

