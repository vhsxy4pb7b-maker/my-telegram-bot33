# 多页面Token管理 - 快速开始

## 问题

当AI系统需要同时管理多个Facebook页面时，每个页面都需要使用自己的Token。如果使用错误的Token，会导致发送消息失败。

## 解决方案

系统已支持**多页面Token自动管理**，会根据消息来源的页面ID自动选择对应的Token。

## 三步配置

### 步骤1: 同步所有页面Token

运行以下命令，自动获取所有可管理页面的Token：

```bash
python scripts/tools/manage_page_tokens.py sync
```

这会：
- ✅ 使用当前 `.env` 中的 `FACEBOOK_ACCESS_TOKEN`
- ✅ 自动获取所有页面的Token
- ✅ 保存到 `.page_tokens.json` 文件

### 步骤2: 验证配置

查看已配置的页面：

```bash
python scripts/tools/manage_page_tokens.py list
```

### 步骤3: 重启服务

重启服务使配置生效：

```bash
python run.py
```

## 工作原理

1. **接收消息** → 系统提取消息中的 `page_id`
2. **查找Token** → 自动在Token管理器中查找该页面的Token
3. **发送消息** → 使用找到的Token发送回复

**无需修改代码**，系统会自动处理！

## 示例

假设您有3个页面：
- 页面A (ID: 122102780061145733)
- 页面B (ID: 474610872412780)  
- 页面C (ID: 800491086479666)

### 配置前

所有消息都使用同一个Token，导致页面B和C的消息发送失败。

### 配置后

```bash
# 1. 同步所有页面Token
python scripts/tools/manage_page_tokens.py sync

# 输出：
# ✅ 成功同步 3 个页面的Token
# 已配置的页面:
#   - An Wei (ID: 122102780061145733)
#   - Iphone Loan Ph 9 (ID: 474610872412780)
#   - iPhone loan 001 (ID: 800491086479666)
```

现在：
- ✅ 收到页面A的消息 → 自动使用页面A的Token回复
- ✅ 收到页面B的消息 → 自动使用页面B的Token回复
- ✅ 收到页面C的消息 → 自动使用页面C的Token回复

## 手动管理

### 添加单个页面Token

```bash
python scripts/tools/manage_page_tokens.py add <page_id> <token> [page_name]
```

示例：
```bash
python scripts/tools/manage_page_tokens.py add 474610872412780 EAAB... "Iphone Loan Ph 9"
```

### 移除页面Token

```bash
python scripts/tools/manage_page_tokens.py remove <page_id>
```

## 常见问题

### Q: 需要修改代码吗？

**A**: 不需要！系统已自动支持多页面Token管理。

### Q: 如果某个页面没有配置Token怎么办？

**A**: 系统会使用默认Token（`.env` 中的 `FACEBOOK_ACCESS_TOKEN`）作为后备。

### Q: Token过期了怎么办？

**A**: 重新运行 `sync` 命令更新所有Token。

### Q: 如何知道哪些页面已配置？

**A**: 运行 `python scripts/tools/manage_page_tokens.py list` 查看。

## 相关文档

- [详细管理指南](MULTI_PAGE_TOKEN_MANAGEMENT.md)
- [页面级Token说明](FACEBOOK_PAGE_TOKEN_EXPLAINED.md)

