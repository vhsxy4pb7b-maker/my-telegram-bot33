# Facebook权限配置 - 最终指南

## 📋 权限需求总结

### 帖子管理功能需要
- ✅ `pages_manage_posts` - 管理页面帖子（发布、删除）

### 广告管理功能需要
- ✅ `ads_read` - 读取广告数据
- ✅ `ads_management` - 管理广告（创建、更新、删除）

### 基础功能需要
- ✅ `pages_messaging` - 发送和接收消息（已有）
- ✅ `pages_read_engagement` - 读取页面互动数据
- ✅ `pages_manage_metadata` - 管理页面元数据（已有）

## 🚀 快速配置方法

### 方法1：使用自动化工具（推荐）

```bash
python setup_facebook_permissions.py
```

这个工具会：
1. ✅ 检查当前权限状态
2. ✅ 生成包含所有权限的授权URL
3. ✅ 在浏览器中打开授权页面
4. ✅ 提取并更新访问令牌
5. ✅ 验证权限配置

### 方法2：手动配置

#### 步骤1：生成授权URL
```bash
python generate_full_permissions_url.py
```

#### 步骤2：授权权限
1. 复制生成的URL
2. 在浏览器中打开
3. 登录并授权所有权限

#### 步骤3：提取令牌
```bash
python extract_token.py
```
粘贴重定向URL，工具会自动提取并更新令牌

#### 步骤4：验证权限
```bash
python check_facebook_permissions.py
```

## 📝 完整权限列表

### OAuth Scope字符串

```
pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management
```

### 权限说明

| 权限 | 用途 | 审查要求 |
|------|------|----------|
| `pages_messaging` | 发送和接收消息 | 不需要 |
| `pages_read_engagement` | 读取页面互动数据 | 不需要 |
| `pages_manage_metadata` | 管理页面元数据 | 不需要 |
| `pages_manage_posts` | 管理页面帖子 | 不需要* |
| `ads_read` | 读取广告数据 | 不需要 |
| `ads_management` | 管理广告 | **需要审查** |

*对于已管理的页面通常不需要审查

## 🔧 可用工具

### 1. 权限检查工具
```bash
python check_facebook_permissions.py
```
- 检查当前令牌的所有权限
- 显示权限状态（已授予/未授予）
- 显示令牌详细信息

### 2. 生成授权URL工具
```bash
python generate_full_permissions_url.py
```
- 自动生成包含所有权限的授权URL
- 可选择在浏览器中自动打开

### 3. 自动化配置工具
```bash
python setup_facebook_permissions.py
```
- 一站式完成所有配置步骤
- 自动检查、生成、授权、更新、验证

### 4. 令牌提取工具
```bash
python extract_token.py
```
- 从重定向URL中提取访问令牌
- 支持自动更新到.env文件

### 5. 交换长期令牌工具
```bash
python exchange_token.py
```
- 将短期令牌交换为长期令牌（60天）

## 📚 相关文档

- `FACEBOOK_PERMISSIONS_GUIDE.md` - 详细权限配置指南
- `QUICK_ADD_PERMISSIONS.md` - 快速添加权限指南
- `PERMISSIONS_SETUP_STEPS.md` - 完整配置步骤
- `PERMISSIONS_SETUP_CHECKLIST.md` - 配置检查清单
- `PERMISSIONS_SUMMARY.md` - 权限总结
- `FACEBOOK_POST_AND_ADS_MANAGEMENT.md` - 功能使用指南

## ⚠️ 重要提示

### 1. ads_management权限审查

如果授权时提示`ads_management`需要审查：
1. 访问：https://developers.facebook.com/apps/848496661333193/app-review/permissions/
2. 找到`ads_management`权限
3. 点击"开始使用"提交审查申请
4. 等待1-3个工作日

### 2. 页面访问令牌

对于帖子管理，建议使用页面访问令牌：

```python
# 获取页面访问令牌
GET /{page-id}?fields=access_token&access_token=USER_ACCESS_TOKEN
```

### 3. 令牌类型

- **短期令牌**：1-2小时（从OAuth获取）
- **长期令牌**：60天（需要交换）
- **页面令牌**：永久（除非撤销）

建议获取长期令牌：
```bash
python exchange_token.py
```

## ✅ 配置完成检查

配置完成后，运行以下命令验证：

```bash
# 检查权限
python check_facebook_permissions.py

# 测试帖子管理功能
python test_facebook_post_ads.py
```

所有检查应显示"✅ 通过"

## 🎯 下一步

配置完成后，您可以：
1. ✅ 使用帖子管理功能发布和管理帖子
2. ✅ 使用广告管理功能管理广告
3. ✅ 运行完整的功能测试

---

**当前状态**：所有工具和文档已准备就绪，可以开始配置权限。




