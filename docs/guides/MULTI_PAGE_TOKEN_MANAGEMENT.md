# 多页面Token管理指南

## 概述

当AI系统需要同时管理多个Facebook页面时，每个页面都需要使用自己的Token。本系统提供了多页面Token管理功能，可以自动根据消息来源的页面ID选择对应的Token。

## 工作原理

### 自动Token选择

系统会根据消息中的 `page_id` 自动选择对应的Token：

1. **接收消息** → 提取 `page_id`
2. **查找Token** → 在Token管理器中查找该页面的Token
3. **发送消息** → 使用找到的Token发送回复

### Token存储

- Token存储在 `.page_tokens.json` 文件中
- 格式：`{页面ID: Token字符串}`
- 支持默认Token（用于未配置的页面）

## 快速开始

### 方法1: 自动同步所有页面Token（推荐）

如果您有用户级别的Token（有 `pages_show_list` 权限），可以一次性同步所有页面的Token：

```bash
python scripts/tools/manage_page_tokens.py sync
```

这会：
1. 使用当前 `.env` 中的 `FACEBOOK_ACCESS_TOKEN`
2. 调用 Facebook API 获取所有可管理的页面
3. 自动保存每个页面的Token到 `.page_tokens.json`

### 方法2: 手动添加页面Token

如果需要手动添加特定页面的Token：

```bash
python scripts/tools/manage_page_tokens.py add <page_id> <token> [page_name]
```

示例：
```bash
python scripts/tools/manage_page_tokens.py add 474610872412780 EAAB... "Iphone Loan Ph 9"
```

### 方法3: 从页面列表获取Token

1. 运行页面ID检查工具：
   ```bash
   python scripts/tools/check_page_id_mismatch.py
   ```

2. 从输出中找到需要的页面和对应的Token

3. 使用 `add` 命令添加

## 管理命令

### 列出所有已配置的页面

```bash
python scripts/tools/manage_page_tokens.py list
```

输出示例：
```
已配置的页面Token
======================================================================

📄 默认Token: 已配置

📋 已配置 3 个页面:
  ✅ An Wei (ID: 122102780061145733)
  ✅ Iphone Loan Ph 9 (ID: 474610872412780)
  ✅ iPhone loan 001 (ID: 800491086479666)
```

### 移除页面Token

```bash
python scripts/tools/manage_page_tokens.py remove <page_id>
```

## 配置文件

Token配置存储在 `.page_tokens.json` 文件中：

```json
{
  "tokens": {
    "default": "EAAB...",
    "122102780061145733": "EAAB...",
    "474610872412780": "EAAB...",
    "800491086479666": "EAAB..."
  },
  "page_info": {
    "122102780061145733": {
      "name": "An Wei",
      "updated_at": "2025-12-13"
    },
    "474610872412780": {
      "name": "Iphone Loan Ph 9",
      "updated_at": "2025-12-13"
    }
  }
}
```

## 工作流程

### 1. 消息接收

当收到Facebook消息时，Webhook事件包含页面ID：

```json
{
  "entry": [{
    "messaging": [{
      "recipient": {
        "id": "474610872412780"  // 这是页面ID
      }
    }]
  }]
}
```

### 2. Token选择

系统自动查找该页面的Token：

```python
# 在 FacebookAPIClient.send_message() 中
if page_id:
    page_token = page_token_manager.get_token(page_id)
    if page_token:
        # 使用页面Token发送消息
```

### 3. 消息发送

使用找到的Token发送回复到对应页面。

## 配置示例

### 场景1: 管理3个页面

```bash
# 1. 同步所有页面Token
python scripts/tools/manage_page_tokens.py sync

# 2. 验证配置
python scripts/tools/manage_page_tokens.py list
```

### 场景2: 只管理特定页面

```bash
# 1. 添加页面1
python scripts/tools/manage_page_tokens.py add 474610872412780 EAAB... "页面1"

# 2. 添加页面2
python scripts/tools/manage_page_tokens.py add 800491086479666 EAAB... "页面2"

# 3. 验证
python scripts/tools/manage_page_tokens.py list
```

## 故障排查

### 问题1: 找不到页面Token

**症状**: 日志显示 "未找到页面 {page_id} 的Token，使用默认Token"

**解决方案**:
1. 运行 `python scripts/tools/manage_page_tokens.py list` 查看已配置的页面
2. 如果页面未配置，运行 `sync` 或 `add` 命令添加

### 问题2: Token过期

**症状**: Facebook API返回401或190错误

**解决方案**:
1. 重新获取页面Token
2. 使用 `add` 命令更新Token

### 问题3: 页面ID不匹配

**症状**: 发送消息失败，但Token有效

**解决方案**:
1. 运行 `python scripts/tools/check_page_id_mismatch.py` 检查
2. 确保Token对应的页面ID与消息中的page_id匹配

## 最佳实践

1. **定期同步Token**
   - 每月运行一次 `sync` 命令
   - 确保所有页面Token都是最新的

2. **设置默认Token**
   - 在 `.env` 中配置 `FACEBOOK_ACCESS_TOKEN` 作为默认Token
   - 用于未配置的页面或作为后备

3. **监控Token状态**
   - 定期运行 `list` 命令检查配置
   - 关注日志中的Token相关警告

4. **备份配置**
   - 定期备份 `.page_tokens.json` 文件
   - 避免Token丢失

## 技术细节

### Token管理器

`PageTokenManager` 类负责：
- 加载和保存Token配置
- 根据page_id查找Token
- 从用户Token同步所有页面Token

### API客户端

`FacebookAPIClient` 类已更新：
- 支持在发送消息时自动选择Token
- 如果找到页面Token，临时使用该Token
- 发送完成后恢复原始Token

## 相关文档

- [页面级Token说明](FACEBOOK_PAGE_TOKEN_EXPLAINED.md)
- [页面ID不匹配解决方案](PAGE_ID_MISMATCH_SOLUTION.md)
- [不回复故障排查](NO_REPLY_TROUBLESHOOTING.md)

