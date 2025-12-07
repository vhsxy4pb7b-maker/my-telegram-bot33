# 🔧 Facebook Webhook 验证失败 - 故障排查指南

## ❌ 错误信息
```
回调 URL 或验证令牌无法验证。请核实提供的信息或稍后重试
```

---

## 🔍 排查步骤（按优先级）

### 步骤 1: 检查回调 URL 是否可访问 ⚠️ 最重要

#### 1.1 确认 URL 格式正确

**正确的格式：**
```
https://你的域名.zeabur.app/webhook
```

**常见错误：**
- ❌ `http://你的域名.zeabur.app/webhook` （缺少 `s`，必须是 HTTPS）
- ❌ `https://你的域名.zeabur.app/webhook/` （末尾多了斜杠）
- ❌ `https://你的域名.zeabur.app` （缺少 `/webhook` 路径）

#### 1.2 测试 URL 是否可访问

在浏览器中访问以下 URL 测试：

**健康检查端点：**
```
https://你的域名.zeabur.app/health
```
应该返回：`{"status": "healthy"}`

**Webhook 验证端点（手动测试）：**
```
https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的令牌&hub.challenge=test123
```
- 如果返回 `test123`，说明端点工作正常
- 如果返回错误或无法访问，说明应用有问题

#### 1.3 检查应用是否运行

1. **在 Zeabur 项目页面：**
   - 查看服务状态是否为 "Running" 或 "运行中"
   - 查看日志，确认没有错误

2. **检查日志：**
   - 在 Zeabur 项目页面 → Logs
   - 确认应用已成功启动
   - 查看是否有错误信息

---

### 步骤 2: 检查验证令牌是否匹配 ⚠️ 第二重要

#### 2.1 获取 Zeabur 中的验证令牌

1. **登录 Zeabur**
   - 访问 https://zeabur.com
   - 进入你的项目

2. **查看环境变量**
   - 点击你的应用服务
   - 进入 "Variables" 或 "环境变量" 标签
   - 找到 `FACEBOOK_VERIFY_TOKEN` 的值
   - **完整复制**这个值（包括所有字符）

#### 2.2 在 Facebook 中使用相同的值

1. **在 Facebook Webhook 设置中：**
   - 打开验证令牌输入框
   - **完全清空**输入框
   - **粘贴**从 Zeabur 复制的值
   - ⚠️ **注意：**
     - 不能有多余的空格
     - 不能有换行符
     - 大小写必须完全一致

#### 2.3 验证令牌格式

**正确的验证令牌示例：**
```
my_secure_token_2024
```

**常见错误：**
- ❌ ` my_secure_token_2024 ` （前后有空格）
- ❌ `my_secure_token_2024\n` （有换行符）
- ❌ `My_Secure_Token_2024` （大小写不一致）

---

### 步骤 3: 检查应用代码逻辑

验证逻辑在 `src/facebook/api_client.py` 中：

```python
async def verify_webhook(self, mode: str, token: str, challenge: str):
    verify_token = settings.facebook_verify_token
    
    if mode == "subscribe" and token == verify_token:
        return challenge
    return None
```

**验证条件：**
1. `mode` 必须是 `"subscribe"`
2. `token` 必须与 `settings.facebook_verify_token` **完全相等**

---

### 步骤 4: 检查路由配置

Webhook 路由在 `src/facebook/webhook_handler.py` 中：

```python
router = APIRouter(prefix="/webhook", tags=["facebook"])

@router.get("")
async def verify_webhook(...):
    ...
```

**正确的 URL 路径：**
- 路由前缀：`/webhook`
- GET 端点：`/webhook`（空字符串表示根路径）
- 完整 URL：`https://你的域名.zeabur.app/webhook`

---

## 🛠️ 详细排查方法

### 方法 1: 手动测试 Webhook 端点

在浏览器中访问（替换为你的实际值）：

```
https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123
```

**预期结果：**
- ✅ 如果返回 `test123`（纯文本），说明验证成功
- ❌ 如果返回 `403 Forbidden`，说明验证令牌不匹配
- ❌ 如果返回 `404 Not Found`，说明 URL 路径错误
- ❌ 如果无法访问，说明应用未运行或 URL 错误

### 方法 2: 查看应用日志

在 Zeabur 项目页面查看日志：

1. **进入 Logs 标签**
2. **查看验证请求日志**
   - 当 Facebook 发送验证请求时，应该能看到日志
   - 查找 "Webhook verified successfully" 或 "Webhook verification failed"

3. **检查错误信息**
   - 如果有错误，日志会显示具体原因

### 方法 3: 使用 curl 测试

在终端中运行（替换为你的实际值）：

```bash
curl "https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的验证令牌&hub.challenge=test123"
```

**预期结果：**
- ✅ 返回 `test123`：验证成功
- ❌ 返回错误：根据错误信息排查

---

## ✅ 常见问题解决方案

### 问题 1: URL 无法访问

**症状：**
- 浏览器显示 "无法访问此网站"
- 或返回 404/500 错误

**解决方法：**
1. 确认 Zeabur 域名正确
2. 确认应用正在运行（查看 Zeabur 服务状态）
3. 确认 URL 格式：`https://域名.zeabur.app/webhook`
4. 等待几分钟让 DNS 生效（如果是新域名）

### 问题 2: 验证令牌不匹配

**症状：**
- URL 可以访问，但验证失败
- 返回 403 Forbidden

**解决方法：**
1. **重新获取验证令牌：**
   - 在 Zeabur 环境变量中查看 `FACEBOOK_VERIFY_TOKEN`
   - 完整复制（包括所有字符）

2. **在 Facebook 中重新输入：**
   - 完全清空输入框
   - 粘贴复制的值
   - 确认没有多余空格

3. **检查环境变量：**
   - 确认 Zeabur 中的 `FACEBOOK_VERIFY_TOKEN` 已设置
   - 确认值不为空
   - 确认没有特殊字符问题

### 问题 3: 应用未运行

**症状：**
- 无法访问任何端点
- Zeabur 显示服务未运行

**解决方法：**
1. **检查服务状态：**
   - 在 Zeabur 项目页面查看服务状态
   - 确认状态为 "Running"

2. **查看部署日志：**
   - 检查是否有部署错误
   - 查看启动日志

3. **重新部署：**
   - 如果服务未运行，点击 "Redeploy"
   - 等待部署完成

### 问题 4: 路由配置错误

**症状：**
- 返回 404 Not Found
- 但健康检查端点可以访问

**解决方法：**
1. **确认路由前缀：**
   - 检查 `src/facebook/webhook_handler.py`
   - 确认 `router = APIRouter(prefix="/webhook")`

2. **确认路由注册：**
   - 检查 `src/main.py`
   - 确认已注册 Facebook 路由

---

## 🔄 完整验证流程

### 1. 准备信息

- [ ] Zeabur 域名：`你的域名.zeabur.app`
- [ ] 验证令牌：从 Zeabur 环境变量获取
- [ ] 应用状态：确认正在运行

### 2. 测试 URL 可访问性

```bash
# 测试健康检查
curl https://你的域名.zeabur.app/health

# 测试 Webhook 端点
curl "https://你的域名.zeabur.app/webhook?hub.mode=subscribe&hub.verify_token=你的令牌&hub.challenge=test123"
```

### 3. 在 Facebook 中配置

1. 访问：https://developers.facebook.com/apps/848496661333193/webhooks/
2. 添加回调 URL：`https://你的域名.zeabur.app/webhook`
3. 输入验证令牌：从 Zeabur 复制的值
4. 点击 "验证并保存"

### 4. 验证结果

- ✅ 如果显示 "已验证"，说明配置成功
- ❌ 如果显示错误，按照上述步骤排查

---

## 📋 检查清单

完成以下所有检查：

- [ ] Zeabur 应用正在运行
- [ ] 可以访问健康检查端点（`/health`）
- [ ] 可以访问 Webhook 端点（`/webhook`）
- [ ] URL 格式正确（`https://域名.zeabur.app/webhook`）
- [ ] 验证令牌已从 Zeabur 环境变量获取
- [ ] 验证令牌在 Facebook 中完全一致（无空格、无换行）
- [ ] 手动测试返回正确的 challenge 值
- [ ] Facebook Webhook 验证成功

---

## 🆘 如果仍然失败

如果完成以上所有步骤仍然失败：

1. **检查 Zeabur 日志：**
   - 查看是否有验证请求的日志
   - 查看是否有错误信息

2. **重新设置验证令牌：**
   - 在 Zeabur 中生成新的验证令牌
   - 在 Facebook 中使用新令牌

3. **检查应用代码：**
   - 确认 `src/config/settings.py` 正确加载环境变量
   - 确认 `src/facebook/api_client.py` 的验证逻辑正确

4. **联系支持：**
   - 提供 Zeabur 日志
   - 提供手动测试结果
   - 提供配置信息（隐藏敏感信息）

---

## 📚 相关文档

- [Facebook Webhook 配置指南](./FACEBOOK_WEBHOOK_SETUP.md)
- [Zeabur 部署指南](./ZEABUR_DEPLOYMENT.md)
- [下一步行动指南](./NEXT_STEPS.md)

