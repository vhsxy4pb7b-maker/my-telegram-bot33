# Facebook OAuth 完整流程指南

## ✅ 当前进度

- ✅ App ID 已配置: 848496661333193
- ✅ 应用域名已配置
- ✅ 授权 URL 正常工作
- ⏳ 等待完成授权获取访问令牌

## 📋 完整流程（5步）

### 步骤 1: 完成授权 ✅ 进行中

在浏览器中：
1. 登录 Facebook 账号
2. 查看应用请求的权限
3. 点击"继续"或"授权"

### 步骤 2: 获取重定向 URL

授权成功后，浏览器地址栏会显示：
```
http://localhost:8000/oauth/callback#access_token=EAABwzLix...&token_type=bearer&expires_in=5183944
```

**重要**: 完整复制这个 URL（包括 `#` 后面的所有内容）

### 步骤 3: 提取访问令牌

运行提取工具：

```bash
python extract_token.py "http://localhost:8000/oauth/callback#access_token=YOUR_TOKEN&token_type=bearer&expires_in=5183944"
```

工具会：
- ✅ 自动提取 access_token
- ✅ 显示令牌信息
- ✅ 询问是否保存到 .env 文件

### 步骤 4: 配置到系统

如果工具已自动保存，可以跳过此步。

否则运行：

```bash
python configure_api_keys.py
```

或手动编辑 `.env` 文件：
```env
FACEBOOK_ACCESS_TOKEN=你的访问令牌
```

### 步骤 5: 交换长期令牌（推荐）

短期令牌只有 1-2 小时，建议交换为长期令牌（60天）：

```bash
python exchange_token.py
```

需要提供：
- 短期访问令牌（刚获取的）
- App ID: 848496661333193
- App Secret（从 Facebook Developer Console 获取）

## 🔑 获取 App Secret

如果需要交换长期令牌，需要 App Secret：

1. 访问: https://developers.facebook.com/apps/848496661333193/settings/basic/
2. 在"应用密钥"（App Secret）旁边点击"显示"
3. 输入密码确认
4. 复制 App Secret

## ✅ 验证配置

配置完成后，验证：

```bash
python verify_setup.py
```

应该看到：
- ✅ FACEBOOK_APP_ID 已配置
- ✅ FACEBOOK_ACCESS_TOKEN 已配置

## 🎯 配置完成后的下一步

1. **测试 Facebook API 连接**
   - 可以测试发送消息功能

2. **配置 Webhook**
   - 在 Facebook Developer Console 中设置 Webhook
   - URL: `https://your-domain.com/webhook`
   - 验证令牌: `.env` 中的 `FACEBOOK_VERIFY_TOKEN`

3. **开始接收消息**
   - 系统可以开始接收 Facebook 消息
   - AI 自动回复功能将启用

## 📝 快速命令参考

```bash
# 提取令牌
python extract_token.py "重定向URL"

# 配置所有 API 密钥
python configure_api_keys.py

# 交换长期令牌
python exchange_token.py

# 验证配置
python verify_setup.py

# 测试 API
python test_api.py
```

## ⚠️ 重要提示

1. **访问令牌安全**
   - 不要分享给他人
   - 不要提交到 Git
   - 妥善保管

2. **令牌有效期**
   - 短期令牌: 1-2 小时
   - 长期令牌: 60 天
   - 建议使用长期令牌

3. **如果授权失败**
   - 检查应用权限设置
   - 确认应用状态正常
   - 查看浏览器控制台错误

## 🆘 需要帮助？

- **详细指南**: `GET_ACCESS_TOKEN.md`
- **完整配置**: `COMPLETE_FACEBOOK_SETUP.md`
- **API 密钥**: `API_KEYS_GUIDE.md`

---

**当前状态**: 等待完成授权获取访问令牌

完成授权后，使用 `python extract_token.py` 提取令牌即可！

