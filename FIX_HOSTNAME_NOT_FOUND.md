# 🔧 修复 HOSTNAME_NOT_FOUND 错误

## ❌ 错误信息
```
04: HOSTNAME_NOT_FOUND
```

这个错误表示 Facebook 无法访问你的 Webhook URL，域名无法解析或应用未正确部署。

---

## 🔍 问题原因

### 可能的原因：
1. **Zeabur 应用未部署或部署失败**
2. **域名未正确配置**
3. **应用服务未运行**
4. **DNS 还未生效（新部署）**
5. **URL 格式错误**

---

## ✅ 解决步骤

### 步骤 1: 检查 Zeabur 应用状态

1. **登录 Zeabur**
   - 访问 https://zeabur.com
   - 进入你的项目

2. **检查服务状态**
   - 查看应用服务的状态
   - 应该显示 "Running" 或 "运行中"
   - 如果显示 "Failed" 或 "Error"，需要修复部署问题

3. **查看部署日志**
   - 点击服务 → Logs
   - 检查是否有部署错误
   - 确认应用已成功启动

### 步骤 2: 获取正确的域名

1. **在 Zeabur 项目页面**
   - 点击你的应用服务
   - 查看 "Domains" 或 "域名" 部分
   - 应该显示类似：`your-service.zeabur.app`

2. **确认域名格式**
   - 正确的格式：`your-service.zeabur.app`
   - 不要包含 `https://` 或路径
   - 完整的 Webhook URL：`https://your-service.zeabur.app/webhook`

### 步骤 3: 测试域名是否可访问

在浏览器中访问以下 URL（替换为你的实际域名）：

1. **健康检查：**
   ```
   https://你的域名.zeabur.app/health
   ```
   - 应该返回：`{"status": "healthy"}`
   - 如果无法访问，说明应用未运行

2. **API 文档：**
   ```
   https://你的域名.zeabur.app/docs
   ```
   - 应该显示 Swagger UI 文档
   - 如果无法访问，说明应用有问题

### 步骤 4: 检查应用部署

如果应用未运行或部署失败：

1. **查看部署日志**
   - 在 Zeabur 项目页面 → Logs
   - 查找错误信息
   - 常见错误：
     - 环境变量缺失
     - 依赖安装失败
     - 启动命令错误

2. **检查环境变量**
   - 确认所有必需的环境变量已设置
   - 特别是 `DATABASE_URL`、`FACEBOOK_VERIFY_TOKEN` 等

3. **重新部署**
   - 如果部署失败，点击 "Redeploy"
   - 等待部署完成（可能需要几分钟）

### 步骤 5: 等待 DNS 生效

如果是新部署：

1. **等待几分钟**
   - 新域名可能需要 1-5 分钟才能生效
   - 等待后再测试

2. **清除浏览器缓存**
   - 使用无痕模式测试
   - 或清除 DNS 缓存

---

## 🧪 验证步骤

### 1. 测试应用是否运行

在浏览器中访问：
```
https://你的域名.zeabur.app/health
```

**预期结果：**
- ✅ 返回 `{"status": "healthy"}`：应用正常运行
- ❌ 无法访问：应用未运行或域名错误

### 2. 测试 Webhook 端点

在浏览器中访问（替换为你的实际值）：
```
https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123
```

**预期结果：**
- ✅ 返回 `test123`：端点工作正常
- ❌ 无法访问：应用未运行或 URL 错误

### 3. 在 Facebook 中重新验证

1. **确认应用已运行**
   - 健康检查端点可以访问

2. **在 Facebook Webhook 设置中**
   - 使用正确的 URL：`https://你的域名.zeabur.app/webhook`
   - 输入正确的验证令牌
   - 点击 "验证并保存"

---

## ⚠️ 常见问题

### 问题 1: 应用部署失败

**症状：**
- Zeabur 显示服务状态为 "Failed"
- 日志中有错误信息

**解决方法：**
1. 查看部署日志，找到错误原因
2. 常见原因：
   - 缺少必需的环境变量
   - 代码错误
   - 依赖安装失败
3. 修复问题后重新部署

### 问题 2: 域名未生成

**症状：**
- 在 Zeabur 中找不到域名
- 或域名显示为 "Pending"

**解决方法：**
1. 等待几分钟让域名生成
2. 如果长时间未生成，检查服务是否正常运行
3. 可以尝试重新部署服务

### 问题 3: DNS 未生效

**症状：**
- 域名存在但无法访问
- 浏览器显示 "无法访问此网站"

**解决方法：**
1. 等待 1-5 分钟让 DNS 生效
2. 使用不同的网络测试
3. 清除 DNS 缓存：
   ```bash
   # Windows
   ipconfig /flushdns
   
   # macOS/Linux
   sudo dscacheutil -flushcache
   ```

### 问题 4: URL 格式错误

**症状：**
- 在 Facebook 中验证失败
- 但应用可以访问

**解决方法：**
1. 确认 URL 格式：
   - ✅ `https://your-service.zeabur.app/webhook`
   - ❌ `http://your-service.zeabur.app/webhook` （缺少 s）
   - ❌ `https://your-service.zeabur.app/webhook/` （末尾有斜杠）
   - ❌ `https://your-service.zeabur.app/webhooks` （路径错误）

---

## 📋 检查清单

完成以下所有检查：

- [ ] Zeabur 应用服务状态为 "Running"
- [ ] 部署日志中没有错误
- [ ] 已获取正确的域名（格式：`your-service.zeabur.app`）
- [ ] 健康检查端点可以访问（`/health`）
- [ ] Webhook 端点可以访问（`/webhook`）
- [ ] URL 格式正确（`https://域名.zeabur.app/webhook`）
- [ ] 等待了足够时间让 DNS 生效（如果是新部署）
- [ ] 在 Facebook 中使用正确的 URL 和验证令牌

---

## 🚀 快速修复流程

1. **检查 Zeabur 服务状态**
   - 确认服务正在运行
   - 如果未运行，查看日志并修复问题

2. **获取域名**
   - 在 Zeabur 项目页面找到应用域名
   - 格式：`your-service.zeabur.app`

3. **测试可访问性**
   - 访问 `https://你的域名.zeabur.app/health`
   - 确认可以访问

4. **在 Facebook 中配置**
   - 使用正确的 URL：`https://你的域名.zeabur.app/webhook`
   - 输入正确的验证令牌
   - 重新验证

---

## 📚 相关文档

- [Webhook 验证故障排查](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
- [Facebook Webhook 配置指南](./FACEBOOK_WEBHOOK_SETUP.md)
- [Zeabur 部署指南](./ZEABUR_DEPLOYMENT.md)

---

如果完成以上步骤仍然无法解决，请提供：
1. Zeabur 服务状态截图
2. 部署日志中的错误信息
3. 测试 URL 的结果

