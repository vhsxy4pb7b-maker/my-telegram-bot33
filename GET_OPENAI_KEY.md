# 🔑 获取 OpenAI API 密钥指南

## 📋 如何获取 OpenAI API 密钥

### 步骤 1: 访问 OpenAI 平台

1. **打开浏览器**，访问: https://platform.openai.com/
2. **登录**你的 OpenAI 账号
   - 如果没有账号，点击 "Sign up" 注册

### 步骤 2: 进入 API Keys 页面

1. 登录后，点击右上角的**头像**或**用户名**
2. 选择 **"API keys"** 或 **"View API keys"**
3. 或者直接访问: https://platform.openai.com/api-keys

### 步骤 3: 创建新的 API 密钥

1. 在 API Keys 页面，点击 **"Create new secret key"** 或 **"+ Create new secret key"**
2. **填写信息**（可选）:
   - 名称: 例如 "Zeabur Deployment" 或 "Customer Service Bot"
3. **点击 "Create secret key"**
4. **重要**: 密钥只会显示一次，**立即复制并保存**！
   - 格式类似: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步骤 4: 保存密钥

**立即保存到安全的地方**：
- 密码管理器
- 文本文件（加密保存）
- 或直接添加到 Zeabur 环境变量

---

## 🔧 在 Zeabur 中配置

### 步骤 1: 打开 Zeabur 环境变量

1. 在 Zeabur 项目页面，点击你的**应用服务**
2. 进入 **"Environment Variables"** 标签

### 步骤 2: 添加或更新 OPENAI_API_KEY

#### 如果变量不存在：
1. 点击 **"Add Variable"** 或 **"+"**
2. 变量名: `OPENAI_API_KEY`
3. 值: 粘贴刚才复制的 API 密钥（sk-... 开头）
4. 点击保存

#### 如果变量已存在（是占位符）：
1. 找到 `OPENAI_API_KEY` 变量
2. 点击**编辑**（铅笔图标）
3. 将值从 `your_openai_api_key` 替换为真实的 API 密钥
4. 点击保存

---

## ✅ 验证配置

1. **确认密钥格式**:
   - 应该以 `sk-` 或 `sk-proj-` 开头
   - 长度通常为 50+ 字符

2. **重新部署**:
   - Zeabur 会自动重新部署
   - 或手动点击 "Redeploy"

3. **检查日志**:
   - 查看部署日志
   - 应该不再有 `openai_api_key Value error` 错误

---

## 💰 OpenAI 计费说明

### 免费额度
- 新账号通常有 $5 免费额度
- 可以用于测试和开发

### 付费
- 使用超出免费额度后需要付费
- 按使用量计费（按 token 数量）

### 查看使用情况
1. 访问: https://platform.openai.com/usage
2. 查看 API 使用量和费用

---

## 🔒 安全提示

1. **不要分享** API 密钥给他人
2. **不要在代码中硬编码** API 密钥
3. **使用环境变量**存储（如 Zeabur）
4. **定期轮换** API 密钥（如果怀疑泄露）
5. **设置使用限制**（在 OpenAI 平台设置）

---

## 🆘 常见问题

### 问题 1: 找不到 API Keys 页面

**解决**:
- 确保已登录 OpenAI 账号
- 直接访问: https://platform.openai.com/api-keys
- 检查账号是否有 API 访问权限

### 问题 2: 无法创建 API 密钥

**可能原因**:
- 账号需要验证
- 需要添加支付方式（即使使用免费额度）
- 账号被限制

**解决**:
- 完成账号验证
- 添加支付方式（即使不付费）
- 联系 OpenAI 支持

### 问题 3: API 密钥无效

**检查**:
- 密钥是否完整复制（没有遗漏字符）
- 密钥是否已过期或被删除
- 是否使用了正确的密钥

**解决**:
- 重新创建新的 API 密钥
- 确保完整复制（包括 sk- 前缀）

---

## 📝 快速步骤总结

1. 访问: https://platform.openai.com/api-keys
2. 登录 OpenAI 账号
3. 点击 "Create new secret key"
4. 复制密钥（格式: sk-...）
5. 在 Zeabur Environment Variables 中添加/更新 `OPENAI_API_KEY`
6. 等待重新部署

---

## 🔗 相关链接

- [OpenAI Platform](https://platform.openai.com/)
- [API Keys 页面](https://platform.openai.com/api-keys)
- [使用情况](https://platform.openai.com/usage)
- [文档](https://platform.openai.com/docs)

---

**获取到 API 密钥后，告诉我，我会帮你配置到 Zeabur！**


