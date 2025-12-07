# 🔧 修复服务无响应问题

## ❌ 错误信息
```
服务无响应，可能是服务未监听正确端口或服务报错崩溃
```

这个错误表示应用无法响应请求，可能的原因：
1. 应用未正确启动
2. 端口配置错误
3. 启动时崩溃
4. 环境变量缺失导致启动失败

---

## 🔍 排查步骤

### 步骤 1: 检查 Zeabur 启动命令配置

#### 1.1 确认启动命令

在 Zeabur 项目页面：

1. **进入应用服务设置**
   - 点击你的应用服务
   - 进入 "Settings" 或 "设置"

2. **检查启动命令 (Start Command)**
   - 应该设置为：
     ```
     uvicorn src.main:app --host 0.0.0.0 --port $PORT
     ```
   - ⚠️ **重要：**
     - 必须使用 `0.0.0.0` 作为 host（不能是 `localhost` 或 `127.0.0.1`）
     - 必须使用 `$PORT` 环境变量（Zeabur 会自动设置）

3. **如果没有启动命令设置**
   - Zeabur 会自动检测 `Procfile`
   - 确认 `Procfile` 存在且内容正确

#### 1.2 检查 Procfile

确认项目根目录有 `Procfile` 文件，内容为：
```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

---

### 步骤 2: 检查环境变量

#### 2.1 必需的环境变量

在 Zeabur 环境变量中，确认以下变量已设置：

**必需变量：**
```
DATABASE_URL=自动提供（Zeabur 会自动设置）
FACEBOOK_APP_ID=你的应用ID
FACEBOOK_APP_SECRET=你的应用密钥
FACEBOOK_ACCESS_TOKEN=你的访问令牌
FACEBOOK_VERIFY_TOKEN=你的验证令牌
OPENAI_API_KEY=你的OpenAI密钥
TELEGRAM_BOT_TOKEN=你的Telegram令牌
TELEGRAM_CHAT_ID=你的Telegram聊天ID
SECRET_KEY=你的安全密钥
```

**可选但推荐：**
```
HOST=0.0.0.0
PORT=$PORT
DEBUG=false
```

#### 2.2 检查环境变量格式

- ✅ 正确：`FACEBOOK_VERIFY_TOKEN=my_token_2024`
- ❌ 错误：`FACEBOOK_VERIFY_TOKEN = my_token_2024` （有空格）
- ❌ 错误：`FACEBOOK_VERIFY_TOKEN="my_token_2024"` （不需要引号）

---

### 步骤 3: 查看部署日志

#### 3.1 在 Zeabur 中查看日志

1. **进入项目页面**
   - 点击你的应用服务
   - 点击 "Logs" 或 "日志" 标签

2. **查找错误信息**
   - 查看最新的日志
   - 查找以下错误：
     - `ImportError` - 导入错误
     - `ModuleNotFoundError` - 模块未找到
     - `ValueError` - 配置错误
     - `ConnectionError` - 数据库连接错误
     - `Port already in use` - 端口被占用

#### 3.2 常见启动错误

**错误 1: 环境变量缺失**
```
ValueError: 请配置有效的Facebook参数
```
**解决：** 检查所有必需的环境变量是否已设置

**错误 2: 数据库连接失败**
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**解决：** 确认 PostgreSQL 服务已添加，`DATABASE_URL` 已自动设置

**错误 3: 端口配置错误**
```
OSError: [Errno 98] Address already in use
```
**解决：** 确保使用 `$PORT` 环境变量，不要硬编码端口

**错误 4: 模块导入错误**
```
ModuleNotFoundError: No module named 'xxx'
```
**解决：** 检查 `requirements.txt` 是否包含所有依赖

---

### 步骤 4: 检查应用启动流程

应用启动时会执行以下步骤：

1. **加载配置**
   - 从环境变量加载配置
   - 如果必需变量缺失，会抛出错误

2. **初始化平台**
   - 初始化 Facebook 和 Instagram 平台
   - 如果配置错误，会显示警告但不会阻止启动

3. **创建数据库表**
   - 自动创建/验证数据库表
   - 如果数据库连接失败，会显示错误

4. **启动服务器**
   - 使用 uvicorn 启动 FastAPI 应用
   - 监听 `0.0.0.0:$PORT`

---

### 步骤 5: 验证服务是否运行

#### 5.1 检查服务状态

在 Zeabur 项目页面：
- 查看服务状态是否为 "Running"
- 如果显示 "Failed" 或 "Error"，查看日志

#### 5.2 测试端点

在浏览器中访问（替换为你的域名）：

1. **健康检查：**
   ```
   https://你的域名.zeabur.app/health
   ```
   - 应该返回：`{"status": "healthy"}`
   - 如果无法访问，说明服务未运行

2. **API 文档：**
   ```
   https://你的域名.zeabur.app/docs
   ```
   - 应该显示 Swagger UI
   - 如果无法访问，说明服务有问题

---

## 🛠️ 修复方法

### 方法 1: 修复启动命令

在 Zeabur 项目页面：

1. **进入应用服务设置**
2. **找到 "Start Command" 或 "启动命令"**
3. **设置为：**
   ```
   uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```
4. **保存并重新部署**

### 方法 2: 修复环境变量

1. **检查所有必需的环境变量**
   - 在 Zeabur 项目页面 → Variables
   - 确认所有变量都已设置
   - 确认值不为空

2. **修复格式错误**
   - 移除多余的空格
   - 移除引号（如果需要）
   - 确认值正确

3. **重新部署**
   - 保存环境变量后，Zeabur 会自动重新部署

### 方法 3: 修复 Procfile

如果使用 Procfile：

1. **确认 Procfile 存在**
   - 在项目根目录
   - 文件名：`Procfile`（没有扩展名）

2. **确认内容正确：**
   ```
   web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

3. **提交并推送：**
   ```bash
   git add Procfile
   git commit -m "修复启动命令"
   git push origin main
   ```

---

## 📋 完整检查清单

完成以下所有检查：

- [ ] Zeabur 启动命令正确：`uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- [ ] Procfile 存在且内容正确
- [ ] 所有必需的环境变量已设置
- [ ] 环境变量值格式正确（无多余空格）
- [ ] PostgreSQL 数据库服务已添加
- [ ] `DATABASE_URL` 已自动设置
- [ ] 服务状态为 "Running"
- [ ] 部署日志中没有错误
- [ ] 健康检查端点可以访问
- [ ] API 文档可以访问

---

## 🧪 测试步骤

### 1. 检查服务状态

在 Zeabur 项目页面：
- 查看服务状态
- 查看最新日志

### 2. 测试端点

在浏览器中访问：
```
https://你的域名.zeabur.app/health
```

**预期结果：**
- ✅ 返回 `{"status": "healthy"}`：服务正常运行
- ❌ 无法访问：服务未运行，需要查看日志

### 3. 查看日志

在 Zeabur Logs 中查找：
- 启动成功信息：`Application startup complete`
- 错误信息：查找 `ERROR` 或 `Exception`

---

## ⚠️ 常见问题

### 问题 1: 端口配置错误

**症状：**
- 服务无法启动
- 日志显示端口错误

**解决：**
1. 确认启动命令使用 `$PORT` 环境变量
2. 不要硬编码端口号
3. 确认 host 为 `0.0.0.0`

### 问题 2: 环境变量缺失

**症状：**
- 启动时抛出 `ValueError`
- 日志显示配置错误

**解决：**
1. 检查所有必需的环境变量
2. 确认值不为空
3. 确认格式正确

### 问题 3: 数据库连接失败

**症状：**
- 启动时数据库连接错误
- 日志显示连接超时

**解决：**
1. 确认 PostgreSQL 服务已添加
2. 确认 `DATABASE_URL` 已自动设置
3. 检查数据库服务是否运行

### 问题 4: 依赖安装失败

**症状：**
- 部署时依赖安装错误
- 模块导入失败

**解决：**
1. 检查 `requirements.txt` 是否正确
2. 确认所有依赖都已列出
3. 查看部署日志中的错误信息

---

## 🚀 快速修复流程

1. **检查启动命令**
   - 确认使用：`uvicorn src.main:app --host 0.0.0.0 --port $PORT`

2. **检查环境变量**
   - 确认所有必需变量已设置
   - 确认值格式正确

3. **查看日志**
   - 查找错误信息
   - 根据错误修复问题

4. **重新部署**
   - 修复后，Zeabur 会自动重新部署
   - 或手动点击 "Redeploy"

5. **验证服务**
   - 等待部署完成
   - 测试健康检查端点

---

## 📚 相关文档

- [Zeabur 部署指南](./ZEABUR_DEPLOYMENT.md)
- [Webhook 验证故障排查](./WEBHOOK_VERIFICATION_TROUBLESHOOTING.md)
- [HOSTNAME_NOT_FOUND 修复](./FIX_HOSTNAME_NOT_FOUND.md)

---

如果完成以上步骤仍然无法解决，请提供：
1. Zeabur 部署日志（特别是错误信息）
2. 服务状态截图
3. 环境变量列表（隐藏敏感信息）

