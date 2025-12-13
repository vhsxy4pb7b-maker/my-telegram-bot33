# Facebook Webhook 事件订阅指南

## 事件类型说明

根据系统代码分析，以下是需要订阅的事件类型及其说明：

## 📋 必需事件

### 1. `messages` - 私信消息

**说明**: 接收 Facebook Messenger 私信消息

**用途**:
- 处理用户发送给页面的消息
- 触发 AI 自动回复
- 收集用户信息

**代码支持**: ✅ 已实现
- 解析器: `FacebookMessageParser._parse_messaging_event()`
- 处理流程: 消息 → 解析 → AI 回复 → 数据收集 → Telegram 通知

**订阅方式**:
在 Facebook 开发者控制台的 Webhook 设置中，勾选 `messages`

---

## 🔔 推荐事件

### 2. `messaging_postbacks` - 按钮点击事件

**说明**: 接收用户点击按钮的事件

**用途**:
- 处理快速回复按钮点击
- 处理 CTA（Call-to-Action）按钮点击
- 处理菜单按钮点击

**代码支持**: ✅ 可通过 `messaging` 事件处理
- 按钮点击事件会通过 `messaging` 事件发送
- 事件中包含 `postback` 字段

**订阅方式**:
在 Facebook 开发者控制台的 Webhook 设置中，勾选 `messaging_postbacks`

**示例事件结构**:
```json
{
  "sender": {"id": "USER_ID"},
  "recipient": {"id": "PAGE_ID"},
  "timestamp": 1234567890,
  "postback": {
    "title": "按钮标题",
    "payload": "BUTTON_PAYLOAD"
  }
}
```

---

### 3. `feed` - 评论事件

**说明**: 接收页面帖子下的评论事件

**用途**:
- 处理用户在页面帖子下的评论
- 自动回复评论
- 收集评论中的用户信息

**代码支持**: ✅ 已实现
- 解析器: `FacebookMessageParser._parse_comment_event()`
- 处理流程: 评论 → 解析 → AI 回复 → 数据收集

**订阅方式**:
在 Facebook 开发者控制台的 Webhook 设置中，勾选 `feed`

**注意事项**:
- 需要页面权限: `pages_read_engagement`
- 只处理新评论（`verb == "add"`）

**示例事件结构**:
```json
{
  "field": "feed",
  "value": {
    "verb": "add",
    "post_id": "POST_ID",
    "comment": {
      "id": "COMMENT_ID",
      "message": "评论内容"
    },
    "from": {
      "id": "USER_ID",
      "name": "用户名"
    }
  }
}
```

---

## 🔧 可选事件

### 4. `messaging_optins` - 用户选择加入事件

**说明**: 接收用户通过插件选择接收消息的事件

**用途**:
- 处理用户通过 Messenger 插件选择加入
- 记录用户选择加入的时间
- 触发欢迎消息

**代码支持**: ⚠️ 可通过 `messaging` 事件处理
- 选择加入事件会通过 `messaging` 事件发送
- 事件中包含 `optin` 字段

**订阅方式**:
在 Facebook 开发者控制台的 Webhook 设置中，勾选 `messaging_optins`

**示例事件结构**:
```json
{
  "sender": {"id": "USER_ID"},
  "recipient": {"id": "PAGE_ID"},
  "timestamp": 1234567890,
  "optin": {
    "ref": "OPTIN_REF",
    "user_ref": "USER_REF"
  }
}
```

---

### 5. `messaging_referrals` - 推荐事件

**说明**: 接收通过推荐链接进入的用户事件

**用途**:
- 处理通过推荐链接进入的用户
- 记录推荐来源
- 触发个性化欢迎消息

**代码支持**: ⚠️ 可通过 `messaging` 事件处理
- 推荐事件会通过 `messaging` 事件发送
- 事件中包含 `referral` 字段

**订阅方式**:
在 Facebook 开发者控制台的 Webhook 设置中，勾选 `messaging_referrals`

**示例事件结构**:
```json
{
  "sender": {"id": "USER_ID"},
  "recipient": {"id": "PAGE_ID"},
  "timestamp": 1234567890,
  "referral": {
    "ref": "REFERRAL_REF",
    "source": "SHORTLINK",
    "type": "OPEN_THREAD"
  }
}
```

---

## 📝 订阅配置步骤

### 在 Facebook 开发者控制台

1. **访问**: https://developers.facebook.com/
2. **选择应用** → **Webhooks** 设置
3. **配置 Webhook**:
   - Callback URL: `https://your-ngrok-url.ngrok-free.dev/webhook`
   - Verify Token: 你的 `FACEBOOK_VERIFY_TOKEN`
   - **Subscription Fields**: 勾选以下事件：
     - ✅ `messages` (必需)
     - ✅ `messaging_postbacks` (推荐)
     - ✅ `feed` (推荐，如果需要处理评论)
     - ⚪ `messaging_optins` (可选)
     - ⚪ `messaging_referrals` (可选)

4. **点击**: "Verify and Save"

### 订阅页面事件

1. 在 **Webhooks** 页面，找到你的页面
2. 点击 **Subscribe** 按钮
3. 选择要订阅的事件类型（与上面相同）

---

## 🎯 推荐配置

### 最小配置（仅处理私信）

```
✅ messages
```

### 标准配置（推荐）

```
✅ messages
✅ messaging_postbacks
✅ feed
```

### 完整配置（所有功能）

```
✅ messages
✅ messaging_postbacks
✅ feed
✅ messaging_optins
✅ messaging_referrals
```

---

## ⚠️ 注意事项

1. **必需权限**:
   - `pages_messaging` - 发送和接收消息（必需）
   - `pages_read_engagement` - 读取评论（如果订阅 `feed`）

2. **事件处理顺序**:
   - 消息事件优先处理
   - 评论事件其次
   - 其他事件按需处理

3. **事件去重**:
   - 系统会自动处理重复事件
   - 使用 `message_id` 进行去重

4. **性能考虑**:
   - 订阅过多事件可能增加服务器负载
   - 建议根据实际需求选择事件类型

---

## 🔍 验证订阅

### 检查 Webhook 状态

1. 在 Facebook 开发者控制台的 Webhook 页面
2. 查看 Webhook 状态（应该是 ✅ 已验证）
3. 查看订阅的页面和事件类型

### 测试事件接收

1. **测试消息**:
   - 向页面发送一条测试消息
   - 查看应用日志: `Get-Content logs\app.log -Tail 50`
   - 应该看到 "Received webhook event"

2. **测试评论**:
   - 在页面帖子下发表评论
   - 查看应用日志
   - 应该看到评论处理日志

3. **测试按钮**:
   - 点击快速回复按钮
   - 查看应用日志
   - 应该看到按钮点击处理日志

---

## 📚 相关文档

- [Facebook Webhook 文档](https://developers.facebook.com/docs/graph-api/webhooks)
- [Messaging Webhooks](https://developers.facebook.com/docs/messenger-platform/webhook)
- [Page Feed Webhooks](https://developers.facebook.com/docs/graph-api/reference/page/feed)

---

## 🛠️ 故障排除

### 问题 1: 消息未收到

**可能原因**:
- 未订阅 `messages` 事件
- 页面未订阅 Webhook
- Webhook URL 配置错误

**解决方法**:
1. 检查 Webhook 订阅状态
2. 检查页面订阅状态
3. 验证 Webhook URL 是否正确

### 问题 2: 评论未收到

**可能原因**:
- 未订阅 `feed` 事件
- 缺少 `pages_read_engagement` 权限

**解决方法**:
1. 订阅 `feed` 事件
2. 申请 `pages_read_engagement` 权限

### 问题 3: 按钮点击未收到

**可能原因**:
- 未订阅 `messaging_postbacks` 事件
- 按钮配置错误

**解决方法**:
1. 订阅 `messaging_postbacks` 事件
2. 检查按钮配置

