# 修复 Facebook 应用域名配置错误

## 错误信息

访问授权 URL 时看到：
```
The domain of this URL isn't included in the app's domains. 
To be able to load this URL, add all domains and subdomains 
of your app to the App Domains field in your app settings.
```

## 解决方案

### 步骤 1: 访问应用设置

直接访问应用设置页面：
```
https://developers.facebook.com/apps/848496661333193/settings/basic/
```

### 步骤 2: 配置应用域名

1. 在"基本"设置页面中，找到"应用域名"（App Domains）字段
2. 添加以下域名：
   ```
   localhost
   ```
3. 点击"保存更改"

### 步骤 3: 配置网站 URL（可选但推荐）

1. 在"基本"设置页面中，找到"网站"部分
2. 点击"添加平台" → 选择"网站"
3. 输入网站 URL：
   ```
   http://localhost:8000
   ```
4. 点击"保存更改"

### 步骤 4: 确认 OAuth 重定向 URI

同时确认"有效的 OAuth 重定向 URI"中已添加：
```
http://localhost:8000/oauth/callback
```

## 完整配置清单

在 Facebook Developer Console 的"基本"设置中，需要配置：

1. ✅ **应用域名（App Domains）**
   - 添加：`localhost`

2. ✅ **网站 URL（Site URL）**
   - 添加：`http://localhost:8000`

3. ✅ **有效的 OAuth 重定向 URI**
   - 添加：`http://localhost:8000/oauth/callback`

## 验证配置

配置完成后：

1. **等待几分钟**让更改生效

2. **重新访问授权 URL**：
   ```
   https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token
   ```

3. **如果配置正确**：
   - 应该能看到 Facebook 登录页面
   - 登录后会显示授权页面

4. **如果仍有错误**：
   - 检查所有配置是否已保存
   - 等待更长时间让更改生效
   - 清除浏览器缓存后重试

## 生产环境配置

如果部署到生产环境，需要：

1. **应用域名**：添加您的实际域名（如：`yourdomain.com`）

2. **网站 URL**：添加您的实际网站 URL（如：`https://yourdomain.com`）

3. **OAuth 重定向 URI**：添加 HTTPS 版本（如：`https://yourdomain.com/oauth/callback`）

## 快速链接

- **应用设置**: https://developers.facebook.com/apps/848496661333193/settings/basic/
- **应用仪表板**: https://developers.facebook.com/apps/848496661333193/dashboard/

