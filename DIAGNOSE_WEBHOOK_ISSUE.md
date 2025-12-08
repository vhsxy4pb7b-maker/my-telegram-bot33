# 🔍 Webhook 验证失败 - 详细诊断指南

## ❌ 问题：一直验证不通过

按照以下步骤逐一排查：

---

## 🔍 第一步：检查应用是否可访问

### 1.1 测试健康检查端点

在浏览器中访问（替换为你的实际域名）：
```
https://你的域名.zeabur.app/health
```

**预期结果：**
- ✅ 返回：`{"status": "healthy"}`
- ❌ 如果无法访问或返回错误，说明应用有问题

**如果无法访问：**
1. 检查 Zeabur 服务状态是否为 "Running"
2. 查看 Zeabur 日志，确认应用已启动
3. 等待 1-2 分钟（如果是新部署）

---

### 1.2 手动测试 Webhook 端点

在浏览器中访问（替换为你的实际值）：
```
https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123
```

**预期结果：**
- ✅ 返回：`test123`（纯文本，不是 JSON）
- ❌ 返回 `403 Forbidden`：验证令牌不匹配
- ❌ 返回 `404 Not Found`：URL 路径错误
- ❌ 返回 `500 Internal Server Error`：应用内部错误

**如果返回 403：**
- 说明验证令牌不匹配
- 继续看第二步

**如果返回 404：**
- 说明 URL 路径错误
- 确认 URL 是：`https://域名.zeabur.app/webhook`（不是 `/webhook/`）

**如果返回 500：**
- 查看 Zeabur 日志，检查错误信息

---

## 🔍 第二步：检查验证令牌

### 2.1 获取 Zeabur 中的验证令牌

1. **登录 Zeabur**：https://zeabur.com
2. **进入你的项目** → **点击你的应用服务**
3. **进入 "Variables" 或 "环境变量"**
4. **找到 `FACEBOOK_VERIFY_TOKEN`**
5. **完整复制这个值**

### 2.2 检查验证令牌格式

**正确的验证令牌：**
- 可以是任何字符串
- 例如：`my_secure_token_2024`
- 例如：`abc123xyz`
- 例如：`token_2024_12_07`

**常见问题：**
- ❌ 前后有空格：` my_token ` → 应该是：`my_token`
- ❌ 有换行符：`my_token\n` → 应该是：`my_token`
- ❌ 大小写不一致：Zeabur 中是 `MyToken`，Facebook 中是 `mytoken`

### 2.3 在 Facebook 中重新输入

1. **完全清空输入框**
   - 选中所有文本（Ctrl+A）
   - 删除
   - 确认输入框完全为空

2. **重新粘贴**
   - 从 Zeabur 复制验证令牌
   - 直接粘贴到 Facebook 输入框
   - 不要手动输入（避免输入错误）

3. **检查粘贴后的值**
   - 确认没有多余空格
   - 确认没有换行符
   - 确认与 Zeabur 中的值完全一致

---

## 🔍 第三步：检查 URL 格式

### 3.1 确认 URL 格式

**正确的格式：**
```
https://你的域名.zeabur.app/webhook
```

**常见错误：**
- ❌ `http://你的域名.zeabur.app/webhook` （缺少 `s`，必须是 HTTPS）
- ❌ `https://你的域名.zeabur.app/webhook/` （末尾多了斜杠）
- ❌ `https://你的域名.zeabur.app` （缺少 `/webhook` 路径）
- ❌ `https://你的域名.zeabur.app/Webhook` （大小写错误，应该是小写 `webhook`）

### 3.2 确认域名正确

1. **在 Zeabur 中确认域名**
   - 进入服务详情页
   - 找到显示的域名
   - 完整复制（包括 `.zeabur.app`）

2. **在 Facebook 中使用相同的域名**
   - 确认域名完全一致
   - 不要手动输入（避免输入错误）

---

## 🔍 第四步：查看应用日志

### 4.1 在 Zeabur 中查看日志

1. **进入 Zeabur 项目页面**
2. **点击你的应用服务**
3. **点击 "Logs" 或 "日志" 标签**
4. **查看最近的日志**

### 4.2 查找验证请求日志

当 Facebook 发送验证请求时，应该能看到：

**成功日志：**
```
Webhook verified successfully
```

**失败日志：**
```
Webhook verification failed
```

**如果没有看到任何日志：**
- 说明 Facebook 的请求没有到达你的应用
- 可能是 URL 错误或应用未运行

**如果看到错误日志：**
- 查看错误信息
- 根据错误信息排查

---

## 🔍 第五步：检查环境变量

### 5.1 确认环境变量已设置

在 Zeabur 中检查：

1. **进入 "Variables" 或 "环境变量"**
2. **确认以下变量已设置：**
   - ✅ `FACEBOOK_VERIFY_TOKEN`（必须有值）
   - ✅ `FACEBOOK_ACCESS_TOKEN`
   - ✅ `FACEBOOK_APP_ID`
   - ✅ `FACEBOOK_APP_SECRET`

### 5.2 确认环境变量值不为空

- `FACEBOOK_VERIFY_TOKEN` 的值不能为空
- 如果为空，需要设置一个值

### 5.3 重新部署（如果修改了环境变量）

如果修改了环境变量：
1. **保存环境变量**
2. **等待应用自动重新部署**
3. **或手动点击 "Redeploy"**
4. **等待部署完成后再测试**

---

## 🔍 第六步：使用 curl 测试（高级）

如果你熟悉命令行，可以使用 curl 测试：

```bash
curl "https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123"
```

**预期结果：**
- ✅ 返回：`test123`
- ❌ 返回错误：根据错误信息排查

---

## 🔍 第七步：检查代码逻辑

验证逻辑在代码中：

```python
async def verify_webhook(self, mode: str, token: str, challenge: str):
    verify_token = settings.facebook_verify_token
    
    if mode == "subscribe" and token == verify_token:
        return challenge
    return None
```

**验证条件：**
1. `mode` 必须是 `"subscribe"`（Facebook 会自动发送）
2. `token` 必须与 `settings.facebook_verify_token` **完全相等**

**如果验证失败，可能原因：**
- `token` 与 `verify_token` 不完全相等（可能有空格、大小写等问题）

---

## 🛠️ 常见问题解决方案

### 问题 1：验证令牌不匹配

**症状：**
- 手动测试返回 403
- Facebook 验证失败

**解决：**
1. 在 Zeabur 中重新复制 `FACEBOOK_VERIFY_TOKEN`
2. 在 Facebook 中完全清空输入框
3. 重新粘贴（不要手动输入）
4. 确认没有多余空格

### 问题 2：URL 无法访问

**症状：**
- 浏览器显示 "无法访问此网站"
- 或返回 404/500 错误

**解决：**
1. 确认应用正在运行（Zeabur 状态为 "Running"）
2. 确认域名正确
3. 确认 URL 格式：`https://域名.zeabur.app/webhook`
4. 等待几分钟让 DNS 生效

### 问题 3：应用未运行

**症状：**
- Zeabur 显示服务未运行
- 无法访问任何端点

**解决：**
1. 查看部署日志，检查错误
2. 检查环境变量是否完整
3. 重新部署应用

### 问题 4：环境变量未加载

**症状：**
- 应用运行但验证失败
- 日志显示验证令牌为空

**解决：**
1. 确认环境变量已设置
2. 确认环境变量值不为空
3. 重新部署应用

---

## 📋 完整排查清单

按照以下顺序逐一检查：

- [ ] 1. 应用健康检查通过（`/health` 返回正常）
- [ ] 2. 手动测试 Webhook 端点返回正确的 challenge
- [ ] 3. 从 Zeabur 获取验证令牌
- [ ] 4. 在 Facebook 中完全清空输入框后重新粘贴
- [ ] 5. URL 格式正确（`https://域名.zeabur.app/webhook`）
- [ ] 6. 域名与 Zeabur 中的完全一致
- [ ] 7. 验证令牌没有多余空格
- [ ] 8. 验证令牌大小写一致
- [ ] 9. 环境变量 `FACEBOOK_VERIFY_TOKEN` 已设置且不为空
- [ ] 10. 应用正在运行（Zeabur 状态为 "Running"）
- [ ] 11. 查看 Zeabur 日志，确认收到验证请求
- [ ] 12. 如果修改了环境变量，已重新部署应用

---

## 🆘 如果仍然失败

如果完成以上所有步骤仍然失败：

### 1. 收集信息

请提供以下信息：

1. **你的域名**：`你的域名.zeabur.app`
2. **手动测试结果**：
   - 访问 `https://你的域名.zeabur.app/health` 的结果
   - 访问 `https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的令牌&hub.challenge=test123` 的结果
3. **Zeabur 日志**：最近的日志截图或文本
4. **Facebook 错误信息**：具体的错误提示

### 2. 重新设置验证令牌

如果问题仍然存在，可以尝试重新设置验证令牌：

1. **在 Zeabur 中生成新令牌**
   - 进入环境变量
   - 修改 `FACEBOOK_VERIFY_TOKEN` 为一个新值（例如：`new_token_2024_12_07`）
   - 保存

2. **等待应用重新部署**

3. **在 Facebook 中使用新令牌**
   - 完全清空输入框
   - 输入新令牌
   - 点击验证

### 3. 检查应用代码

如果问题仍然存在，可能需要检查：
- 应用是否正确加载环境变量
- 路由是否正确配置
- 验证逻辑是否正确

---

## 📚 相关文档

- [一步步操作指南](./STEP_BY_STEP_WEBHOOK_SETUP.md)
- [Webhook 配置快速参考](./WEBHOOK_CONFIG_QUICK_REFERENCE.md)
- [故障排查指南](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)

---

## 💡 提示

1. **最重要**：验证令牌必须与 Zeabur 环境变量中的值完全一致
2. **最常见错误**：验证令牌前后有空格
3. **测试顺序**：先测试 `/health`，再测试 `/webhook`，最后在 Facebook 中验证
4. **耐心等待**：修改环境变量后，需要等待应用重新部署

