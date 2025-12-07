# 快速添加Facebook权限指南

## 当前权限状态

根据权限检查结果，您的访问令牌当前缺少以下权限：

### 缺失的权限

1. **pages_read_engagement** - 读取页面互动数据
2. **pages_manage_posts** - 管理页面帖子（发布、删除）
3. **ads_read** - 读取广告数据
4. **ads_management** - 管理广告

## 快速添加权限步骤

### 方法1：重新生成OAuth授权URL（推荐）

#### 步骤1：生成包含所有权限的授权URL

运行以下命令或使用脚本：

```python
# 包含所有权限的OAuth URL
oauth_url = f"""
https://www.facebook.com/v18.0/dialog/oauth?
  client_id=YOUR_APP_ID
  &redirect_uri=YOUR_REDIRECT_URI
  &scope=pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management
  &response_type=token
"""
```

#### 步骤2：使用现有工具生成URL

```bash
python generate_oauth_url.py
```

然后手动修改scope参数，添加缺失的权限。

#### 步骤3：访问授权URL

1. 在浏览器中打开生成的URL
2. 登录Facebook账号
3. 授权所有请求的权限
4. 从重定向URL中提取新的访问令牌

#### 步骤4：更新访问令牌

在`.env`文件中更新：

```env
FACEBOOK_ACCESS_TOKEN=新的访问令牌
```

### 方法2：在Facebook Developer Console中添加

#### 步骤1：访问应用设置

1. 访问 https://developers.facebook.com/
2. 选择您的应用（App ID: 848496661333193）
3. 进入"应用审查" → "权限和功能"

#### 步骤2：添加权限

找到以下权限并点击"添加"：

1. **pages_read_engagement**
   - 用途：读取页面互动数据
   - 审查要求：通常不需要审查

2. **pages_manage_posts**
   - 用途：管理页面帖子
   - 审查要求：通常不需要审查（对于已管理的页面）

3. **ads_read**
   - 用途：读取广告数据
   - 审查要求：通常不需要审查

4. **ads_management**
   - 用途：管理广告
   - 审查要求：**需要应用审查**

#### 步骤3：重新授权

添加权限后，需要重新生成访问令牌：

1. 使用新的OAuth URL（包含所有权限）
2. 重新授权
3. 获取新的访问令牌

### 方法3：使用Graph API Explorer

#### 步骤1：访问Graph API Explorer

1. 访问 https://developers.facebook.com/tools/explorer/
2. 选择您的应用（848496661333193）

#### 步骤2：选择权限

在"权限"下拉菜单中，选择或添加：

- pages_messaging
- pages_read_engagement
- pages_manage_metadata
- pages_manage_posts
- ads_read
- ads_management

#### 步骤3：生成访问令牌

1. 点击"生成访问令牌"
2. 授权所有权限
3. 复制生成的访问令牌

#### 步骤4：更新配置

在`.env`文件中更新访问令牌。

## 完整OAuth Scope字符串

```
pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management
```

## 验证权限

添加权限后，运行权限检查工具验证：

```bash
python check_facebook_permissions.py
```

应该看到所有权限都显示为"✅ 已授予"。

## 注意事项

### 1. 应用审查

`ads_management`权限需要应用审查：
- 访问"应用审查" → "权限和功能"
- 找到`ads_management`
- 点击"开始使用"提交审查申请
- 等待1-3个工作日

### 2. 页面访问令牌

对于帖子管理功能，建议使用**页面访问令牌**（Page Access Token）而不是用户访问令牌：

```python
# 获取页面访问令牌
GET /{page-id}?fields=access_token&access_token=USER_ACCESS_TOKEN
```

### 3. 权限生效时间

- 新添加的权限需要重新授权才能生效
- 旧的访问令牌不会自动获得新权限
- 必须重新生成访问令牌

## 快速命令参考

### 检查当前权限
```bash
python check_facebook_permissions.py
```

### 生成OAuth URL
```bash
python generate_oauth_url.py
```

### 交换长期令牌
```bash
python exchange_token.py
```

## 相关文档

- `FACEBOOK_PERMISSIONS_GUIDE.md` - 详细权限配置指南
- `FACEBOOK_OAUTH_GUIDE.md` - OAuth授权完整指南
- `GET_ACCESS_TOKEN.md` - 获取访问令牌指南





