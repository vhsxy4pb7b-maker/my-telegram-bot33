# Facebook权限总结

## 权限分类

### 基础权限（消息功能）

| 权限 | 用途 | 审查要求 |
|------|------|----------|
| `pages_messaging` | 发送和接收消息 | 不需要 |
| `pages_read_engagement` | 读取页面互动数据 | 不需要 |
| `pages_manage_metadata` | 管理页面元数据 | 不需要 |

### 帖子管理权限

| 权限 | 用途 | 审查要求 |
|------|------|----------|
| `pages_manage_posts` | 管理页面帖子（发布、删除） | 不需要* |

*对于已管理的页面通常不需要审查

### 广告管理权限

| 权限 | 用途 | 审查要求 |
|------|------|----------|
| `ads_read` | 读取广告数据 | 不需要 |
| `ads_management` | 管理广告（创建、更新、删除） | **需要审查** |

## 完整权限列表

### 所有功能权限

```
pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts,ads_read,ads_management
```

### 仅消息功能

```
pages_messaging,pages_read_engagement,pages_manage_metadata
```

### 消息 + 帖子管理

```
pages_messaging,pages_read_engagement,pages_manage_metadata,pages_manage_posts
```

### 消息 + 广告管理

```
pages_messaging,pages_read_engagement,pages_manage_metadata,ads_read,ads_management
```

## 检查权限

运行权限检查工具：

```bash
python check_facebook_permissions.py
```

## 添加权限

参考以下文档：
- `QUICK_ADD_PERMISSIONS.md` - 快速添加权限指南
- `FACEBOOK_PERMISSIONS_GUIDE.md` - 详细权限配置指南

## 相关功能

### 需要pages_manage_posts的功能
- `create_post()` - 发布帖子
- `delete_post()` - 删除帖子
- `get_post()` - 获取帖子信息

### 需要ads_read的功能
- `get_ad_accounts()` - 获取广告账户
- `get_ads()` - 获取广告列表
- `get_ad()` - 获取广告信息
- `get_campaigns()` - 获取广告系列
- `get_adsets()` - 获取广告组

### 需要ads_management的功能
- `create_ad()` - 创建广告
- `update_ad()` - 更新广告
- `delete_ad()` - 删除广告




