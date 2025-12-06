# Facebook OAuth 配置总结

## 快速开始

### 如果您已有 App ID

```bash
python setup_facebook_quick.py YOUR_APP_ID
```

### 如果您还没有 App ID

1. 访问 https://developers.facebook.com/
2. 创建应用（选择"业务"类型）
3. 获取 App ID
4. 然后运行上面的命令

## 完整配置流程

### 步骤 1: 获取 App ID

- 访问 Facebook Developer Console
- 创建应用
- 在"设置" → "基本"中获取 App ID

### 步骤 2: 配置重定向 URI

在 Facebook Developer Console 中：
- 设置 → 基本 → 有效的 OAuth 重定向 URI
- 添加：`http://localhost:8000/oauth/callback`

### 步骤 3: 生成授权 URL

```bash
python setup_facebook_quick.py YOUR_APP_ID
```

### 步骤 4: 获取访问令牌

1. 在浏览器中打开生成的授权 URL
2. 登录并授权
3. 从重定向 URL 中提取 `access_token`

### 步骤 5: 配置到系统

```bash
python configure_api_keys.py
```

或手动编辑 `.env` 文件。

### 步骤 6: 交换长期令牌（可选）

```bash
python exchange_token.py
```

## 可用工具

| 工具 | 用途 | 命令 |
|------|------|------|
| `setup_facebook_quick.py` | 快速生成授权 URL | `python setup_facebook_quick.py APP_ID` |
| `setup_facebook_complete.py` | 完整设置向导 | `python setup_facebook_complete.py` |
| `exchange_token.py` | 交换长期令牌 | `python exchange_token.py` |
| `configure_api_keys.py` | 配置 API 密钥 | `python configure_api_keys.py` |

## 文档

- `FACEBOOK_OAUTH_GUIDE.md` - 详细 OAuth 指南
- `API_KEYS_GUIDE.md` - API 密钥获取指南
- `OAUTH_QUICK_START.md` - 快速开始

## 需要帮助？

如果遇到问题，请查看：
- `FACEBOOK_OAUTH_GUIDE.md` - 常见问题解答
- `API_KEYS_GUIDE.md` - 获取 App ID 的详细步骤

