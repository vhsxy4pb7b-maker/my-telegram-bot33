# 如何打开 Facebook 授权页面

## 🚀 快速打开授权页面

### 方法 1: 自动打开（推荐）

运行以下命令，会自动在浏览器中打开授权页面：

```bash
python generate_oauth_url.py 848496661333193
```

或者使用完整工具：

```bash
python setup_facebook_quick.py 848496661333193
```

### 方法 2: 手动打开

在浏览器中访问以下 URL：

```
https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token
```

### 方法 3: 使用 PowerShell 打开

在 PowerShell 中运行：

```powershell
Start-Process "https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token"
```

## 📋 授权流程

### 步骤 1: 登录 Facebook

1. 授权页面打开后，您会看到 Facebook 登录界面
2. 输入您的 Facebook 账号和密码
3. 点击"登录"按钮

### 步骤 2: 授权应用

登录成功后，您会看到授权页面，显示应用请求的权限：

- ✅ **pages_messaging** - 发送和接收消息
- ✅ **pages_read_engagement** - 读取页面互动数据
- ✅ **pages_manage_metadata** - 管理页面元数据

点击 **"继续"** 或 **"授权"** 按钮。

### 步骤 3: 获取访问令牌

授权成功后，浏览器会自动重定向到：

```
http://localhost:8000/oauth/callback#access_token=...
```

回调页面会显示访问令牌信息。

## ⚠️ 重要提示

### 确保回调服务运行

在授权之前，确保回调服务正在运行：

```bash
python oauth_callback_handler.py
```

或者启动主服务：

```bash
python run.py
```

### 如果授权页面无法打开

1. **检查网络连接**
   - 确保可以访问 Facebook

2. **检查应用配置**
   - 确保应用域名已配置（`localhost`）
   - 确保重定向 URI 已配置（`http://localhost:8000/oauth/callback`）

3. **手动复制 URL**
   - 如果自动打开失败，手动复制 URL 到浏览器

## 🔧 授权 URL 参数说明

- **client_id**: `848496661333193` (您的 Facebook App ID)
- **redirect_uri**: `http://localhost:8000/oauth/callback` (回调地址)
- **scope**: `pages_messaging,pages_read_engagement,pages_manage_metadata` (权限范围)
- **response_type**: `token` (返回访问令牌)

## 📝 授权完成后

授权成功后，您会看到重定向页面，然后：

1. **复制重定向 URL**（浏览器地址栏中的完整 URL）
2. **运行提取工具**：
   ```bash
   python extract_token.py "完整的重定向URL"
   ```
3. **或直接告诉我重定向 URL**，我会帮您提取令牌

## 🆘 需要帮助？

如果遇到问题：
- 查看 `AUTHORIZATION_HELP.md` 获取详细帮助
- 查看 `FIND_REDIRECT_URL.md` 了解如何找到重定向 URL
- 告诉我具体错误信息，我会帮您解决

