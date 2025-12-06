# Facebook OAuth 快速开始

## 快速生成授权 URL

### 方法 1: 使用命令行参数

```bash
python generate_oauth_url.py YOUR_APP_ID
```

### 方法 2: 交互式输入

```bash
python generate_oauth_url.py
```

然后输入您的 Facebook App ID。

### 方法 3: 使用完整工具

```bash
python facebook_oauth_helper.py
```

## 授权 URL 格式

```
https://www.facebook.com/v18.0/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=pages_messaging,pages_read_engagement
  &response_type=token
```

## 完整流程

1. **生成授权 URL**
   ```bash
   python generate_oauth_url.py YOUR_APP_ID
   ```

2. **在浏览器中打开 URL**

3. **登录并授权**

4. **获取访问令牌**
   - 从重定向 URL 中提取 `access_token`
   - 格式：`http://localhost:8000/oauth/callback#access_token=TOKEN&...`

5. **交换长期令牌（可选）**
   ```bash
   python exchange_token.py
   ```

6. **配置到系统**
   ```bash
   python configure_api_keys.py
   ```

## 需要帮助？

- 查看 `FACEBOOK_OAUTH_GUIDE.md` 获取详细说明
- 查看 `API_KEYS_GUIDE.md` 了解如何获取 App ID

