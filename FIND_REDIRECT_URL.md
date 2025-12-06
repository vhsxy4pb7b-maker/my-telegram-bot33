# 如何找到重定向 URL

## 📍 重定向 URL 的位置

重定向 URL 会显示在**浏览器地址栏**中，授权成功后会自动跳转到这个页面。

## 🔍 查找步骤

### 步骤 1: 查看浏览器窗口

授权成功后，浏览器会自动跳转到一个新页面，页面标题可能是：
- "Facebook OAuth 回调"
- "OAuth 回调"
- 或显示访问令牌信息的页面

### 步骤 2: 查看浏览器地址栏

在浏览器窗口的**顶部地址栏**中，您会看到类似这样的 URL：

```
http://localhost:8000/oauth/callback#access_token=EAABwzLixNjYBO7ZC...&token_type=bearer&expires_in=5183944
```

**重要：** 这是重定向 URL，包含了访问令牌信息。

### 步骤 3: 复制完整 URL

1. **点击地址栏**，选中整个 URL
2. **复制**（Ctrl+C 或右键复制）
3. **完整复制**，包括 `#` 后面的所有内容

## 📋 重定向 URL 的格式

重定向 URL 的格式如下：

```
http://localhost:8000/oauth/callback#access_token=TOKEN&token_type=bearer&expires_in=SECONDS
```

**组成部分：**
- `http://localhost:8000/oauth/callback` - 回调地址
- `#access_token=...` - 访问令牌（这是最重要的部分）
- `&token_type=bearer` - 令牌类型
- `&expires_in=5183944` - 过期时间（秒）

## 🔍 如果找不到重定向 URL

### 情况 1: 授权尚未完成

**检查：**
- 是否已登录 Facebook？
- 是否已点击"授权"按钮？
- 是否看到了授权成功的提示？

**解决：**
- 返回授权页面完成授权
- 确保点击了"授权"而不是"取消"

### 情况 2: 页面在新标签中打开

**检查：**
- 查看所有浏览器标签页
- 查找地址包含 `localhost:8000/oauth/callback` 的标签

**解决：**
- 切换到包含回调 URL 的标签页
- 复制地址栏中的 URL

### 情况 3: 回调服务未运行

**检查：**
- 回调服务是否正在运行？
- 是否看到了"无法连接"的错误？

**解决：**
- 运行 `python oauth_callback_handler.py` 启动服务
- 或运行 `python run.py` 启动主服务

### 情况 4: 授权被拒绝或失败

**检查：**
- 是否看到了错误页面？
- 浏览器地址栏显示什么？

**解决：**
- 重新访问授权 URL
- 确保完成授权流程

## 📝 找到重定向 URL 后

### 方法 1: 使用提取工具（推荐）

复制完整的重定向 URL，然后运行：

```bash
python extract_token.py "完整的重定向URL"
```

工具会自动：
- 提取访问令牌
- 显示令牌信息
- 询问是否保存到 .env 文件

### 方法 2: 手动提取

从 URL 中找到 `access_token=` 后面的值（到 `&` 之前）。

例如，如果 URL 是：
```
http://localhost:8000/oauth/callback#access_token=EAABwzLixNjYBO7ZC...&token_type=bearer
```

那么访问令牌就是：`EAABwzLixNjYBO7ZC...`（整个值）

### 方法 3: 直接告诉我

如果您找到了重定向 URL，可以直接告诉我，我会帮您提取并配置。

## 💡 提示

1. **重定向 URL 很长**，包含完整的访问令牌
2. **必须完整复制**，包括 `#` 后面的所有内容
3. **访问令牌是敏感信息**，不要分享给他人
4. **如果页面显示了令牌信息**，也可以直接复制页面上的令牌

## 🆘 需要帮助？

如果仍然找不到重定向 URL，请告诉我：
1. 授权是否已完成？
2. 浏览器中看到了什么页面？
3. 浏览器地址栏显示什么？

我会帮您解决！

