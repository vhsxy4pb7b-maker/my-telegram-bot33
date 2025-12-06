# 配置 Facebook OAuth 重定向 URI 详细指南

## 当前应用信息

- **App ID**: 848496661333193
- **重定向 URI**: http://localhost:8000/oauth/callback

## 配置步骤（详细）

### 步骤 1: 访问 Facebook Developer Console

1. 打开浏览器
2. 访问：https://developers.facebook.com/
3. 使用您的 Facebook 账号登录

### 步骤 2: 选择您的应用

1. 在顶部导航栏，点击"我的应用"
2. 在应用列表中找到您的应用
   - 如果应用列表很长，可以使用搜索功能
   - 或直接访问：https://developers.facebook.com/apps/848496661333193/settings/basic/

### 步骤 3: 进入基本设置

1. 在左侧菜单中，点击"设置"
2. 在下拉菜单中选择"基本"
3. 或直接访问：https://developers.facebook.com/apps/848496661333193/settings/basic/

### 步骤 4: 配置 OAuth 重定向 URI

1. 在"基本"设置页面中，向下滚动
2. 找到"有效的 OAuth 重定向 URI"部分
3. 点击"添加 URI"或"+"按钮
4. 输入以下 URI：
   ```
   http://localhost:8000/oauth/callback
   ```
5. 点击"保存更改"或"保存"

### 步骤 5: 验证配置

1. 确认 URI 已添加到列表中
2. 检查 URI 格式是否正确（没有多余的空格或字符）
3. 保存后等待几秒钟让更改生效

## 重要提示

### ⚠️ 注意事项

1. **URI 必须完全匹配**
   - 协议：必须是 `http://`（本地开发）或 `https://`（生产环境）
   - 域名：`localhost`（本地）或您的实际域名（生产）
   - 端口：`8000`（如果使用其他端口需要相应修改）
   - 路径：`/oauth/callback`（必须完全匹配）

2. **本地开发 vs 生产环境**
   - 本地开发：`http://localhost:8000/oauth/callback`
   - 生产环境：`https://your-domain.com/oauth/callback`
   - 可以同时添加多个 URI

3. **常见错误**
   - ❌ 忘记添加 `http://` 或 `https://`
   - ❌ 端口号错误
   - ❌ 路径拼写错误
   - ❌ 有多余的空格

## 验证配置

配置完成后，可以：

1. **测试授权 URL**
   - 使用之前生成的授权 URL
   - 在浏览器中打开
   - 如果配置正确，授权后会重定向到您的 URI

2. **检查错误信息**
   - 如果看到 "redirect_uri_mismatch" 错误
   - 说明 URI 配置不正确，请检查拼写和格式

## 快速链接

- **应用设置页面**: https://developers.facebook.com/apps/848496661333193/settings/basic/
- **应用仪表板**: https://developers.facebook.com/apps/848496661333193/dashboard/

## 下一步

配置完成后：

1. **获取访问令牌**
   - 在浏览器中打开授权 URL
   - 授权后获取访问令牌

2. **提取令牌**
   ```bash
   python extract_token.py "重定向URL"
   ```

3. **配置到系统**
   ```bash
   python configure_api_keys.py
   ```

## 需要帮助？

如果遇到问题：
- 检查 URI 格式是否正确
- 确认已保存更改
- 等待几分钟让更改生效
- 查看 Facebook 开发者文档

