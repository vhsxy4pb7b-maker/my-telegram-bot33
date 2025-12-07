# Instagram平台快速开始指南

## 前置条件

1. ✅ 已完成Facebook平台配置
2. ✅ 已运行数据库迁移：`alembic upgrade head`
3. ✅ Instagram Business账户已连接到Facebook页面

## 快速配置步骤

### 1. 获取Instagram User ID

Instagram User ID是发送消息所必需的。获取方法：

#### 方法1：通过Graph API Explorer

1. 访问 [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. 选择您的应用
3. 获取访问令牌（需要 `instagram_basic` 权限）
4. 查询：`GET /me/accounts`
5. 找到连接的Instagram账户，获取 `instagram_business_account.id`

#### 方法2：通过API查询

```bash
curl -X GET "https://graph.facebook.com/v18.0/{page-id}?fields=instagram_business_account&access_token={access-token}"
```

### 2. 配置环境变量

在 `.env` 文件中添加（可选，未设置则使用Facebook配置）：

```env
# Instagram配置（可选）
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token  # 可选，默认使用FACEBOOK_ACCESS_TOKEN
INSTAGRAM_VERIFY_TOKEN=your_instagram_verify_token   # 可选，默认使用FACEBOOK_VERIFY_TOKEN
INSTAGRAM_USER_ID=your_instagram_user_id            # 必需，用于发送消息
```

**注意**：
- `INSTAGRAM_USER_ID` 是**必需的**，如果没有配置，系统无法发送Instagram消息
- 其他两个配置项是可选的，未设置时会自动使用Facebook的配置

### 3. 配置Instagram Webhook

#### 在Facebook Developer Console中：

1. 访问您的应用设置
2. 进入"产品" → "Instagram"
3. 添加"Instagram Messaging"产品
4. 配置Webhook：
   - **回调URL**: `https://your-domain.com/instagram/webhook`
   - **验证令牌**: 使用 `.env` 中的 `INSTAGRAM_VERIFY_TOKEN` 或 `FACEBOOK_VERIFY_TOKEN`
5. 订阅事件：
   - ✅ `messages` - Instagram私信

### 4. 验证配置

运行验证脚本：

```bash
python verify_platform_setup.py
```

应该看到：
```
✅ Instagram平台已注册
✅ Instagram配置: ACCESS_TOKEN 已配置
✅ Instagram配置: VERIFY_TOKEN 已配置
✅ Instagram配置: USER_ID 已配置
```

### 5. 启动系统

```bash
python run.py
```

### 6. 测试Webhook

#### 验证Webhook

```bash
curl "http://localhost:8000/instagram/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test123"
```

应该返回：`test123`

#### 发送测试消息

1. 在Instagram上向您的Instagram Business账户发送私信
2. 系统应该：
   - ✅ 接收消息
   - ✅ 自动回复（如果配置了AI）
   - ✅ 保存到数据库
   - ✅ 发送Telegram通知（如果需要审核）

## 常见问题

### Q: Instagram消息未接收

**检查项**：
1. Webhook URL是否正确配置
2. 验证令牌是否匹配
3. Instagram Business账户是否已连接Facebook页面
4. 是否订阅了 `messages` 事件

### Q: 无法发送Instagram消息

**原因**：`INSTAGRAM_USER_ID` 未配置或配置错误

**解决**：
1. 确认已获取正确的Instagram User ID
2. 在 `.env` 中配置 `INSTAGRAM_USER_ID`
3. 重启应用

### Q: 系统显示Instagram平台未初始化

**检查**：
1. 运行 `python verify_platform_setup.py` 查看详细错误
2. 检查访问令牌是否有效
3. 查看应用日志获取错误信息

## API端点

### Webhook验证
```
GET /instagram/webhook?hub.mode=subscribe&hub.verify_token={token}&hub.challenge={challenge}
```

### Webhook接收
```
POST /instagram/webhook
```

## 功能支持

### ✅ 已支持
- Instagram私信接收
- Instagram私信自动回复
- 资料自动收集
- 智能过滤
- Telegram通知
- 人工审核

### ❌ 暂不支持
- Instagram评论（API限制）
- Instagram Story回复（需要额外权限）

## 下一步

配置完成后，您可以：
1. 测试发送和接收消息
2. 配置AI自动回复规则
3. 设置过滤规则
4. 配置Telegram通知

## 相关文档

- `INSTAGRAM_SETUP.md` - 详细配置指南
- `README.md` - 系统总览
- `verify_platform_setup.py` - 配置验证工具





