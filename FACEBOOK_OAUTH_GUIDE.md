# Facebook OAuth 授权指南

## 概述

要获取 Facebook 长期访问令牌（Long-lived Access Token），需要使用 OAuth 授权流程。

## 授权 URL 格式

```
https://www.facebook.com/v18.0/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=pages_messaging,pages_read_engagement
  &response_type=token
```

## 参数说明

- **client_id**: Facebook 应用 ID（App ID）
- **redirect_uri**: 授权后的重定向地址（需要在 Facebook 应用中配置）
- **scope**: 权限范围
  - `pages_messaging` - 发送和接收消息
  - `pages_read_engagement` - 读取页面互动数据
  - `pages_manage_metadata` - 管理页面元数据
- **response_type**: 响应类型，使用 `token` 获取访问令牌

## 使用工具生成授权 URL

运行以下命令：

```bash
python facebook_oauth_helper.py
```

工具会：
1. 读取或询问 Facebook App ID
2. 生成完整的授权 URL
3. 可选择在浏览器中自动打开

## 手动生成授权 URL

### 步骤 1: 准备信息

- Facebook App ID（从 Facebook Developer Console 获取）
- 重定向 URI（例如：`http://localhost:8000/oauth/callback`）

### 步骤 2: 在 Facebook 应用中配置重定向 URI

1. 访问 https://developers.facebook.com/
2. 选择您的应用
3. 进入"设置" → "基本"
4. 在"有效的 OAuth 重定向 URI"中添加您的重定向 URI

### 步骤 3: 构建授权 URL

替换以下 URL 中的参数：

```
https://www.facebook.com/v18.0/dialog/oauth?
  client_id=YOUR_APP_ID
  &redirect_uri=http://localhost:8000/oauth/callback
  &scope=pages_messaging,pages_read_engagement,pages_manage_metadata
  &response_type=token
```

### 步骤 4: 在浏览器中打开

1. 复制完整的授权 URL
2. 在浏览器中打开
3. 登录 Facebook 账号
4. 授权应用权限

### 步骤 5: 获取访问令牌

授权成功后，浏览器会重定向到：

```
http://localhost:8000/oauth/callback#access_token=YOUR_ACCESS_TOKEN&token_type=bearer&expires_in=5183944
```

从 URL 的 fragment（# 后面的部分）中提取 `access_token` 的值。

## 配置访问令牌

获取访问令牌后，有两种方式配置：

### 方法 1: 使用配置工具

```bash
python configure_api_keys.py
```

在提示时输入访问令牌。

### 方法 2: 手动编辑 .env 文件

打开 `.env` 文件，更新：

```env
FACEBOOK_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
```

## 获取长期访问令牌

默认获取的是短期令牌（1-2 小时）。要获取长期令牌（60 天）：

### 使用 Graph API

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?
  grant_type=fb_exchange_token&
  client_id=YOUR_APP_ID&
  client_secret=YOUR_APP_SECRET&
  fb_exchange_token=SHORT_LIVED_TOKEN"
```

### 使用 Python 脚本

创建 `exchange_token.py`：

```python
import requests
from src.config import settings

short_token = "YOUR_SHORT_LIVED_TOKEN"
app_id = settings.facebook_app_id
app_secret = settings.facebook_app_secret

url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": short_token
}

response = requests.get(url, params=params)
data = response.json()

if "access_token" in data:
    print(f"长期访问令牌: {data['access_token']}")
    print(f"过期时间: {data.get('expires_in', 'N/A')} 秒")
else:
    print(f"错误: {data}")
```

## 常见问题

### 问题 1: 重定向 URI 不匹配

**错误**: `redirect_uri_mismatch`

**解决方案**:
- 确保在 Facebook 应用中配置了正确的重定向 URI
- 重定向 URI 必须完全匹配（包括协议、域名、端口、路径）

### 问题 2: 权限被拒绝

**错误**: 用户拒绝授权

**解决方案**:
- 确保请求的权限是应用所需的
- 检查应用是否已通过 Facebook 审核（某些权限需要审核）

### 问题 3: 令牌过期

**解决方案**:
- 使用短期令牌交换长期令牌
- 或设置自动刷新机制

## 安全提示

⚠️ **重要**:
- 永远不要将访问令牌提交到 Git
- 定期轮换访问令牌
- 使用环境变量存储敏感信息
- 生产环境使用 HTTPS

## 下一步

获取访问令牌后：
1. 配置到 `.env` 文件
2. 测试 Facebook API 连接
3. 配置 Webhook
4. 开始接收消息

