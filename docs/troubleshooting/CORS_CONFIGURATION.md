# CORS配置说明

## 什么是CORS？

CORS（Cross-Origin Resource Sharing，跨域资源共享）是一种安全机制，用于控制哪些域名可以访问您的API。

## 警告信息

```
生产环境未配置CORS_ORIGINS，将拒绝所有跨域请求。
```

## 是否需要配置CORS？

### 情况1: 纯Webhook服务（不需要CORS）

如果您的应用**只作为Webhook接收服务**（Facebook、Instagram、Telegram等），**不需要配置CORS**。

**原因**：
- Webhook是服务器到服务器的通信，不涉及浏览器跨域
- Facebook、Instagram等平台直接调用您的API，不需要CORS
- 不配置CORS更安全，拒绝所有跨域请求

**处理方式**：
- 可以忽略此警告
- 或者设置 `CORS_ORIGINS=`（空字符串）明确表示不需要CORS

### 情况2: 有前端管理界面（需要CORS）

如果您的应用**有前端管理界面**（如React、Vue等前端应用），**需要配置CORS**。

**配置方法**：

1. **在Zeabur环境变量中配置**：
   ```
   CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
   ```

2. **多个域名用逗号分隔**：
   ```
   CORS_ORIGINS=https://admin.example.com,https://dashboard.example.com,https://app.example.com
   ```

3. **支持HTTP和HTTPS**：
   ```
   CORS_ORIGINS=http://localhost:3000,https://production-domain.com
   ```

## 配置步骤

### 在Zeabur中配置

1. 登录Zeabur控制台
2. 进入您的项目
3. 找到"Environment Variables"（环境变量）设置
4. 添加新的环境变量：
   - **Key**: `CORS_ORIGINS`
   - **Value**: 您的域名列表（逗号分隔）
5. 保存并重新部署

### 示例配置

**单域名**：
```
CORS_ORIGINS=https://admin.yourdomain.com
```

**多域名**：
```
CORS_ORIGINS=https://admin.yourdomain.com,https://dashboard.yourdomain.com
```

**开发和生产环境**：
```
CORS_ORIGINS=http://localhost:3000,https://admin.yourdomain.com
```

## 验证配置

配置后，重启服务，警告应该消失。如果仍有警告，检查：

1. 环境变量名称是否正确：`CORS_ORIGINS`（全大写）
2. 环境变量值格式是否正确（逗号分隔，无空格）
3. 服务是否已重启

## 安全建议

1. **生产环境**：
   - 只配置您实际需要的前端域名
   - 不要使用 `*` 允许所有来源
   - 使用HTTPS域名

2. **开发环境**：
   - 可以配置 `CORS_ORIGINS=*` 或本地开发域名
   - 但生产环境必须限制为具体域名

3. **Webhook服务**：
   - 如果只有Webhook，可以不配置CORS
   - 这样更安全，拒绝所有跨域请求

## 常见问题

### Q: 这个警告会影响功能吗？

**A**: 
- 如果只有Webhook服务：**不影响**，可以忽略
- 如果有前端界面：**会影响**，前端无法访问API，需要配置

### Q: 如何判断是否需要CORS？

**A**: 
- 如果只有Facebook/Instagram/Telegram Webhook：**不需要**
- 如果有浏览器访问的前端界面：**需要**

### Q: 配置后警告还在怎么办？

**A**: 
1. 确认环境变量已保存
2. 重启服务
3. 检查环境变量名称和格式
4. 查看日志确认配置已加载

## 相关文档

- [部署指南 - CORS配置](../deployment/DEPLOYMENT_GUIDE.md#cors配置)
- [环境变量配置](../deployment/DEPLOYMENT_GUIDE.md#环境变量配置)

---

**最后更新**: 2025-12-13  
**版本**: 1.0.0

