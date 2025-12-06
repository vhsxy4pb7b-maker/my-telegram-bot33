# Facebook 应用完整配置指南

## 当前状态

- **App ID**: 848496661333193
- **错误**: 应用域名未配置

## 必须配置的项目

### 1. 应用域名（App Domains）⚠️ 必需

**位置**: 设置 → 基本 → 应用域名

**添加**: 
```
localhost
```

**为什么需要**: Facebook 需要知道您的应用可以使用哪些域名

### 2. 网站 URL（Site URL）⚠️ 必需

**位置**: 设置 → 基本 → 网站

**步骤**:
1. 点击"添加平台"
2. 选择"网站"
3. 输入:
```
http://localhost:8000
```

### 3. OAuth 重定向 URI ⚠️ 必需

**位置**: 设置 → 基本 → 有效的 OAuth 重定向 URI

**添加**:
```
http://localhost:8000/oauth/callback
```

## 详细配置步骤

### 步骤 1: 访问应用设置

直接访问（最快）:
```
https://developers.facebook.com/apps/848496661333193/settings/basic/
```

或手动导航:
1. 访问 https://developers.facebook.com/
2. 点击"我的应用"
3. 选择应用 ID: 848496661333193
4. 左侧菜单 → 设置 → 基本

### 步骤 2: 配置应用域名

1. 在"基本"设置页面中，向下滚动
2. 找到"应用域名"（App Domains）字段
3. 在输入框中输入: `localhost`
4. 不要包含 `http://` 或端口号，只输入域名

### 步骤 3: 添加网站平台

1. 在"基本"设置页面中，找到"网站"部分
2. 如果没有"网站"部分，点击"添加平台"按钮
3. 选择"网站"
4. 在"网站 URL"中输入: `http://localhost:8000`
5. 保存

### 步骤 4: 配置 OAuth 重定向 URI

1. 在"基本"设置页面中，找到"有效的 OAuth 重定向 URI"
2. 点击"添加 URI"或"+"按钮
3. 输入: `http://localhost:8000/oauth/callback`
4. 保存

### 步骤 5: 保存所有更改

1. 滚动到页面底部
2. 点击"保存更改"按钮
3. 等待确认消息

### 步骤 6: 等待生效

- 通常需要 1-5 分钟
- 可以刷新页面确认更改已保存

## 配置检查清单

在保存前，确认以下项目都已配置：

- [ ] 应用域名: `localhost`
- [ ] 网站 URL: `http://localhost:8000`
- [ ] OAuth 重定向 URI: `http://localhost:8000/oauth/callback`
- [ ] 所有更改已保存

## 验证配置

配置完成后，重新访问授权 URL:

```
https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata&response_type=token
```

**成功标志**:
- ✅ 看到 Facebook 登录页面
- ✅ 登录后看到授权页面
- ✅ 授权后重定向到 `http://localhost:8000/oauth/callback`

**失败标志**:
- ❌ 仍然显示域名错误
- ❌ 显示 redirect_uri_mismatch 错误

## 常见问题

### Q: 找不到"应用域名"字段？

**A**: 
- 确保在"基本"设置页面
- 可能需要向下滚动
- 某些应用类型可能字段位置不同

### Q: 保存后仍然报错？

**A**: 
- 等待 5-10 分钟让更改生效
- 清除浏览器缓存
- 使用无痕模式重试
- 检查所有三个配置项是否都正确

### Q: 可以添加多个域名吗？

**A**: 
- 可以，用逗号分隔
- 例如: `localhost,example.com`

## 快速链接

- **应用设置**: https://developers.facebook.com/apps/848496661333193/settings/basic/
- **应用仪表板**: https://developers.facebook.com/apps/848496661333193/dashboard/
- **产品设置**: https://developers.facebook.com/apps/848496661333193/dashboard/

## 配置完成后

1. **获取访问令牌**
   - 使用授权 URL 获取令牌

2. **提取令牌**
   ```bash
   python extract_token.py "重定向URL"
   ```

3. **配置到系统**
   ```bash
   python configure_api_keys.py
   ```

4. **交换长期令牌**（可选）
   ```bash
   python exchange_token.py
   ```

