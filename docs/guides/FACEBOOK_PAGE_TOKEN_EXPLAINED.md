# Facebook 页面级 Access Token 详解

## 什么是页面级 Access Token？

**页面级 Access Token（Page Access Token）** 是指**特定 Facebook 页面（Page）的权限令牌**，而不是您个人账户的权限。

### 关键概念

1. **Facebook 页面（Page）**
   - 这是您在 Facebook 上创建的**业务页面**或**品牌页面**
   - 每个页面都有唯一的**页面ID**（Page ID）
   - 例如：您的公司页面、产品页面、粉丝专页等

2. **页面级 Token vs 用户级 Token**
   - **用户级 Token**：代表您个人账户的权限
   - **页面级 Token**：代表**某个特定页面**的权限

3. **为什么需要页面级 Token？**
   - Facebook Messenger API 要求使用页面级 Token 来发送消息
   - 只有页面级 Token 才能代表页面与用户进行对话
   - 用户级 Token 无法直接发送 Messenger 消息

## 如何确定是哪个页面？

### 方法 1: 查看页面ID

当您获取页面级 Token 时，会看到页面信息：

```json
{
  "data": [
    {
      "access_token": "EAAB...",  // 这是页面级Token
      "category": "Product/Service",
      "name": "我的公司页面",      // 页面名称
      "id": "122102780061145733",  // 页面ID
      "tasks": ["MANAGE", "CREATE_CONTENT", "MODERATE", "ADVERTISE", "ANALYZE"]
    }
  ]
}
```

### 方法 2: 使用 Token 查询页面信息

在 Graph API Explorer 中：

1. 使用您的页面级 Token
2. 输入: `GET /me?fields=id,name,category`
3. 返回的信息就是该 Token 对应的页面

**示例返回**：
```json
{
  "id": "122102780061145733",
  "name": "我的公司页面",
  "category": "Product/Service"
}
```

### 方法 3: 查看 Webhook 事件

当收到消息时，Webhook 事件中会包含页面ID：

```json
{
  "entry": [{
    "messaging": [{
      "recipient": {
        "id": "122102780061145733"  // 这就是页面ID
      },
      "sender": {
        "id": "USER_ID"
      }
    }]
  }]
}
```

## 如何获取特定页面的 Token？

### 步骤 1: 获取您管理的所有页面列表

1. 访问 [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. 选择您的应用
3. 生成用户 Token（需要 `pages_show_list` 权限）
4. 调用: `GET /me/accounts`
5. 您会看到所有您管理的页面列表

### 步骤 2: 选择目标页面

从返回的列表中找到您要使用的页面：

```json
{
  "data": [
    {
      "access_token": "EAAB...",
      "name": "页面A",
      "id": "PAGE_ID_A"
    },
    {
      "access_token": "EAAB...",
      "name": "页面B", 
      "id": "PAGE_ID_B"
    }
  ]
}
```

### 步骤 3: 复制对应页面的 Token

- 如果您要使用"页面A"，复制页面A的 `access_token`
- 如果您要使用"页面B"，复制页面B的 `access_token`

## 在系统中如何使用？

### 当前配置

在 `.env` 文件中：

```env
FACEBOOK_ACCESS_TOKEN=EAAB...（某个页面的Token）
```

这个 Token 对应的是**您在获取时选择的那个页面**。

### 多页面支持

如果您的应用需要管理多个页面，可以：

1. **为每个页面配置不同的 Token**
   - 在代码中根据 `page_id` 使用不同的 Token
   - 需要修改代码以支持多 Token 配置

2. **使用页面ID区分**
   - 系统已经支持通过 `page_id` 参数指定页面
   - 但当前所有操作都使用同一个 Token（`.env` 中配置的）

## 如何验证 Token 对应的页面？

### 使用配置检查工具

运行：

```bash
python scripts/tools/check_and_fix_config.py
```

工具会显示：
```
✅ Token有效
用户/页面: 页面名称 (ID: 页面ID)
```

这里的"页面名称"和"页面ID"就是该 Token 对应的页面。

### 手动验证

在 Graph API Explorer 中：

1. 使用您的 Token
2. 调用: `GET /me?fields=id,name`
3. 查看返回的 `name` 和 `id`，这就是该 Token 对应的页面

## 常见问题

### Q: 我有多个页面，应该用哪个页面的 Token？

**A**: 使用您要接收和发送消息的那个页面的 Token。通常这是您的主要业务页面。

### Q: 如何知道当前 Token 是哪个页面的？

**A**: 
1. 运行配置检查工具
2. 或在 Graph API Explorer 中调用 `GET /me?fields=id,name`

### Q: 可以同时使用多个页面的 Token 吗？

**A**: 当前系统配置只支持一个 Token。如果需要多页面支持，需要修改代码以支持多 Token 配置。

### Q: 页面 Token 过期了怎么办？

**A**: 
1. 重新获取该页面的 Token（使用 `GET /me/accounts`）
2. 更新 `.env` 文件中的 `FACEBOOK_ACCESS_TOKEN`
3. 重启应用

### Q: 页面 Token 和页面ID的关系？

**A**: 
- **页面ID**：页面的唯一标识符（数字）
- **页面Token**：该页面的访问令牌（字符串，以 EAAB 开头）
- 一个页面ID对应一个页面Token
- 不同页面有不同的Token

## 总结

- **页面级 Access Token** = **特定 Facebook 页面的权限令牌**
- 它代表的是您在 Facebook 上创建的**某个业务页面**，而不是您的个人账户
- 每个页面都有自己的 Token
- 当前系统使用 `.env` 中配置的 Token，对应一个特定页面
- 可以通过 `GET /me?fields=id,name` 查询 Token 对应的页面信息

