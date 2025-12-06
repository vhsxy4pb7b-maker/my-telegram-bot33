# OAuth 授权 - 下一步操作

## 当前状态

✅ 授权 URL 已正常工作
⏳ 等待完成授权流程

## 操作步骤

### 步骤 1: 在浏览器中完成授权

1. **登录 Facebook**
   - 在授权页面输入您的 Facebook 账号和密码
   - 点击"登录"

2. **授权应用**
   - 查看应用请求的权限
   - 点击"继续"或"授权"按钮

### 步骤 2: 获取重定向 URL

授权成功后，浏览器会自动重定向到：

```
http://localhost:8000/oauth/callback#access_token=YOUR_TOKEN&token_type=bearer&expires_in=5183944
```

**重要提示**：
- 完整复制浏览器地址栏中的 URL
- 包括 `#` 后面的所有内容
- 这是获取访问令牌的关键

### 步骤 3: 提取访问令牌

有两种方式：

#### 方式 1: 使用提取工具（推荐）

```bash
python extract_token.py "完整的重定向URL"
```

工具会自动：
- 提取 access_token
- 显示令牌信息
- 询问是否保存到 .env 文件

#### 方式 2: 使用回调处理器（自动显示）

如果服务正在运行，授权后会自动显示令牌信息页面。

启动回调处理器：
```bash
python oauth_callback_handler.py
```

然后在浏览器中完成授权，页面会自动显示访问令牌。

### 步骤 4: 配置到系统

如果提取工具已自动保存，可以跳过。

否则运行：
```bash
python configure_api_keys.py
```

### 步骤 5: 交换长期令牌（推荐）

```bash
python exchange_token.py
```

需要提供 App Secret。

## 快速命令

```bash
# 提取令牌（授权后）
python extract_token.py "重定向URL"

# 或使用回调处理器（自动显示）
python oauth_callback_handler.py

# 配置所有密钥
python configure_api_keys.py

# 交换长期令牌
python exchange_token.py

# 验证配置
python verify_setup.py
```

## 提示

1. **如果看不到重定向页面**
   - 检查服务是否运行（`python run.py`）
   - 或直接复制浏览器地址栏的 URL

2. **访问令牌格式**
   - 通常以 `EAAB` 或 `EAA` 开头
   - 长度约 200+ 字符

3. **令牌有效期**
   - 短期：1-2 小时
   - 长期：60 天（推荐）

## 需要帮助？

- 查看 `GET_ACCESS_TOKEN.md` 获取详细说明
- 查看 `OAUTH_COMPLETE_GUIDE.md` 获取完整流程

