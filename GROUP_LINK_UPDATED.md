# 群组链接已更新 ✅

## 📋 更新内容

已将Telegram群组链接更新为实际链接：

**群组链接**: `https://t.me/+Yz6RzEdD7JZjOGU1`

**群组信息**:
- 群组名称: 📱iPhone loan Chat(2)
- 成员数: 1,520
- 在线人数: 24

## ✅ 已完成的更新

### 1. 提示词文件更新
- ✅ `src/ai/prompts/iphone_loan_telegram.py` 
- ✅ 所有 `@your_group` 和 `@your_channel` 已替换为实际链接
- ✅ 第一条消息中的群组邀请已更新

### 2. 配置文件更新
- ✅ `config.yaml` 已添加群组配置
- ✅ 已启用 `iphone_loan_telegram` 提示词类型

## 🚀 下一步

1. **重启服务**使配置生效：
   ```bash
   python run.py
   ```

2. **测试机器人**：
   - 发送第一条消息，应该自动包含群组链接
   - 每2-3条消息会提醒加入群组

## 📝 配置详情

当前配置 (`config.yaml`):

```yaml
ai_templates:
  prompt_type: "iphone_loan_telegram"

telegram_groups:
  main_group: "https://t.me/+Yz6RzEdD7JZjOGU1"
```

## ✨ 功能说明

现在机器人会：
- ✅ 第一条消息自动发送群组邀请链接
- ✅ 自动识别用户输入（iPhone型号、金额等）
- ✅ 每2-3条消息提醒加入群组
- ✅ 自动推进贷款申请流程

## 🔗 群组链接

用户可以通过以下链接加入群组：
👉 https://t.me/+Yz6RzEdD7JZjOGU1

