# Facebook权限配置完整流程

## 当前状态

根据权限检查，您的访问令牌缺少以下权限：
- ⚠️ `pages_read_engagement` - 读取页面互动数据
- ⚠️ `pages_manage_posts` - 管理页面帖子（发布、删除）
- ⚠️ `ads_read` - 读取广告数据
- ⚠️ `ads_management` - 管理广告（创建、更新、删除）

## 完整配置流程

### 步骤1：检查当前权限 ✅

已运行：
```bash
python check_facebook_permissions.py
```

**结果**：缺少4个权限

### 步骤2：生成OAuth授权URL ✅

已生成包含所有权限的授权URL：

```
https://www.facebook.com/v18.0/dialog/oauth?client_id=848496661333193&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&scope=pages_messaging%2Cpages_read_engagement%2Cpages_manage_metadata%2Cpages_manage_posts%2Cads_read%2Cads_management&response_type=token
```

**包含的权限**：
- ✅ pages_messaging
- ✅ pages_read_engagement
- ✅ pages_manage_metadata
- ✅ pages_manage_posts
- ✅ ads_read
- ✅ ads_management

### 步骤3：授权并获取新令牌

#### 3.1 打开授权URL

1. 复制上面的URL
2. 在浏览器中打开
3. 登录您的Facebook账号

#### 3.2 授权权限

1. 查看请求的权限列表
2. 点击"继续"或"授权"按钮
3. 确认授权所有权限

#### 3.3 提取访问令牌

授权成功后，浏览器会重定向到：
```
http://localhost:8000/oauth/callback#access_token=新的访问令牌&token_type=bearer&expires_in=...
```

**提取方法**：
1. 从URL的`#access_token=`后面复制令牌
2. 令牌会一直复制到`&`符号之前
3. 或者使用提取工具：`python extract_token.py`

### 步骤4：更新访问令牌

#### 方法1：手动更新.env文件

编辑`.env`文件，更新：
```env
FACEBOOK_ACCESS_TOKEN=新的访问令牌
```

#### 方法2：使用配置工具

```bash
python configure_api_keys.py
```

### 步骤5：验证权限 ✅

运行权限检查工具验证新令牌：

```bash
python check_facebook_permissions.py
```

**预期结果**：所有权限应显示为"✅ 已授予"

## 快速命令

### 生成授权URL
```bash
python generate_full_permissions_url.py
```

### 检查权限
```bash
python check_facebook_permissions.py
```

### 提取令牌（从重定向URL）
```bash
python extract_token.py
```

## 注意事项

### 1. ads_management权限审查

`ads_management`权限可能需要应用审查：
- 如果授权时提示需要审查，请访问Facebook Developer Console
- 进入"应用审查" → "权限和功能"
- 找到`ads_management`并提交审查申请
- 等待1-3个工作日

### 2. 页面访问令牌

对于帖子管理功能，建议使用**页面访问令牌**：

```python
# 获取页面访问令牌
GET /{page-id}?fields=access_token&access_token=USER_ACCESS_TOKEN
```

### 3. 令牌过期

- 短期令牌：通常1-2小时
- 长期令牌：60天
- 建议使用长期令牌

交换长期令牌：
```bash
python exchange_token.py
```

## 故障排除

### 问题1：授权后没有重定向

**解决**：
1. 检查重定向URI是否正确配置
2. 确保应用域名已配置
3. 检查浏览器控制台是否有错误

### 问题2：某些权限无法授权

**解决**：
1. 检查权限是否在应用中启用
2. 某些权限可能需要应用审查
3. 查看Facebook Developer Console中的权限状态

### 问题3：授权后权限仍然缺失

**解决**：
1. 确保使用了新的访问令牌
2. 重新运行权限检查工具
3. 检查令牌是否包含所需权限

## 相关文档

- `FACEBOOK_PERMISSIONS_GUIDE.md` - 详细权限配置指南
- `QUICK_ADD_PERMISSIONS.md` - 快速添加权限指南
- `PERMISSIONS_SUMMARY.md` - 权限总结





