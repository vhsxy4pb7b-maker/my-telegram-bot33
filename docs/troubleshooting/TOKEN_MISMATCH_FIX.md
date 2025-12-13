# Facebook页面Token不匹配问题修复指南

## 问题描述

当看到以下错误日志时，表示页面Token与页面ID不匹配：

```
Facebook API 400 error for page XXXXX: (#10) Requested Page Does Not Match Page Access Token
```

## 问题原因

- 页面Token被错误地分配给错误的页面ID
- Token已过期或被撤销
- Token权限不足

## 诊断步骤

### 1. 运行诊断工具

```bash
python scripts/tools/diagnose_page_token_mismatch.py
```

这个工具会：
- 检查所有配置的页面
- 验证每个Token是否属于正确的页面
- 显示Token的权限信息
- 提供详细的诊断报告

### 2. 查看诊断结果

诊断工具会显示：
- ✅ **正常**: Token有效且匹配
- ❌ **Token不匹配**: Token属于其他页面
- ⚠️ **Token未配置**: 页面没有Token

## 修复方法

### 方法1: 自动修复（如果Token只是被交换）

如果诊断显示Token被交换了（例如：页面A的Token属于页面B，页面B的Token属于页面A），可以使用自动修复工具：

```bash
python scripts/tools/fix_page_token_mismatch.py
```

这个工具会：
- 自动交换不匹配的Token
- 备份原配置文件
- 验证修复结果

### 方法2: 手动更新Token

如果自动修复无法解决问题，需要手动获取正确的Token：

1. **获取正确的页面Token**

   访问 Facebook Developer Console:
   - https://developers.facebook.com/apps/
   - 选择你的应用
   - 进入 "Tools" > "Graph API Explorer"
   - 选择正确的页面
   - 获取页面Token

2. **验证Token**

   访问 Token调试工具:
   - https://developers.facebook.com/tools/debug/accesstoken/
   - 输入Token
   - 确认Token属于正确的页面

3. **更新Token**

   使用页面管理工具:
   ```bash
   python scripts/tools/manage_pages.py
   ```

   或直接编辑 `.page_tokens.json` 文件:
   ```json
   {
     "tokens": {
       "your_page_id": "your_correct_token_here"
     },
     "page_info": {
       "your_page_id": {
         "name": "页面名称"
       }
     }
   }
   ```

### 方法3: 从用户Token同步

如果你有用户级别的Token（有 `pages_show_list` 权限），可以自动同步所有页面Token：

```bash
python scripts/tools/manage_pages.py
# 选择 "从用户Token同步所有页面"
```

## 应用修复

### 重要：重启服务

修复Token后，**必须重启服务**才能应用更改：

**Linux/macOS:**
```bash
# 如果使用systemd
sudo systemctl restart facebook-customer-service

# 或直接重启
pkill -f "python.*run.py"
python run.py
```

**Windows:**
```powershell
# 停止当前服务（Ctrl+C）
# 然后重新启动
python run.py
```

### 验证修复

重启后，运行诊断工具确认修复成功：

```bash
python scripts/tools/diagnose_page_token_mismatch.py
```

所有页面应该显示 ✅ Token有效且匹配。

## 预防措施

### 1. 定期检查Token

定期运行Token检查：

```bash
# 检查Token过期
python scripts/tools/check_token_expiry.py

# 检查Token匹配
python scripts/tools/diagnose_page_token_mismatch.py
```

### 2. 使用长期Token

确保使用长期Token（60天有效期）：

```bash
python scripts/tools/convert_to_long_lived_token.py
```

### 3. 设置Token过期预警

定期检查Token过期状态，提前更新：

```bash
python scripts/tools/check_token_expiry.py
```

## 常见问题

### Q: 修复后仍然看到错误？

A: 确保已重启服务。如果问题仍然存在，检查：
1. Token是否真的属于正确的页面
2. Token是否已过期
3. Token是否有足够的权限（需要 `pages_messaging` 权限）

### Q: 如何获取正确的页面Token？

A: 
1. 访问 Facebook Developer Console
2. 使用 Graph API Explorer
3. 选择正确的页面
4. 获取页面Token

### Q: 可以自动重新加载Token吗？

A: 当前版本需要重启服务。未来版本可能会添加热重载功能。

## 相关工具

- `diagnose_page_token_mismatch.py` - 诊断Token不匹配
- `fix_page_token_mismatch.py` - 自动修复Token不匹配
- `check_token_expiry.py` - 检查Token过期
- `manage_pages.py` - 管理页面Token
- `update_all_tokens_now.py` - 更新所有Token

## 技术支持

如果问题仍然存在，请：
1. 运行诊断工具并保存输出
2. 检查日志文件 `logs/app.log`
3. 提交Issue到GitHub仓库

