# Facebook权限配置检查清单

## 配置前检查

- [ ] 已运行 `python check_facebook_permissions.py` 检查当前权限
- [ ] 已确认缺失的权限
- [ ] 已了解所需权限的用途

## 配置步骤

### 步骤1：生成授权URL
- [ ] 运行 `python generate_full_permissions_url.py`
- [ ] 已复制生成的授权URL

### 步骤2：授权权限
- [ ] 在浏览器中打开授权URL
- [ ] 已登录Facebook账号
- [ ] 已查看请求的权限列表
- [ ] 已点击"继续"或"授权"按钮
- [ ] 已成功授权所有权限

### 步骤3：提取访问令牌
- [ ] 已从重定向URL中提取access_token
- [ ] 已复制完整的访问令牌

### 步骤4：更新配置
- [ ] 已更新.env文件中的FACEBOOK_ACCESS_TOKEN
- [ ] 或已使用配置工具更新令牌

### 步骤5：验证权限
- [ ] 已运行 `python check_facebook_permissions.py`
- [ ] 所有权限显示为"✅ 已授予"

## 权限检查清单

### 基础权限
- [ ] `pages_messaging` - 发送和接收消息
- [ ] `pages_read_engagement` - 读取页面互动数据
- [ ] `pages_manage_metadata` - 管理页面元数据

### 帖子管理权限
- [ ] `pages_manage_posts` - 管理页面帖子

### 广告管理权限
- [ ] `ads_read` - 读取广告数据
- [ ] `ads_management` - 管理广告（如需要审查，已提交）

## 功能测试清单

### 帖子管理功能
- [ ] 可以发布帖子（`create_post`）
- [ ] 可以删除帖子（`delete_post`）
- [ ] 可以获取帖子信息（`get_post`）

### 广告管理功能
- [ ] 可以获取广告账户（`get_ad_accounts`）
- [ ] 可以获取广告列表（`get_ads`）
- [ ] 可以获取广告信息（`get_ad`）
- [ ] 可以创建广告（`create_ad`）- 需要ads_management
- [ ] 可以更新广告（`update_ad`）- 需要ads_management
- [ ] 可以删除广告（`delete_ad`）- 需要ads_management

## 完成确认

- [ ] 所有权限已授予
- [ ] 所有功能测试通过
- [ ] 已更新相关文档
- [ ] 已备份新的访问令牌

## 下一步

配置完成后，您可以：
1. 使用帖子管理功能发布和管理帖子
2. 使用广告管理功能管理广告
3. 运行完整的功能测试





