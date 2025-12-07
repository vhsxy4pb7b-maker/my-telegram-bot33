# iPhone Loan Telegram Bot - Quick Setup

## 🚀 快速配置（3步）

### 1. 启用专用提示词

编辑 `config.yaml`，添加：

```yaml
ai_templates:
  prompt_type: "iphone_loan_telegram"
```

### 2. 配置Telegram群组/频道

编辑 `src/ai/prompts/iphone_loan_telegram.py`，替换：

```python
👉 @your_group    # 替换为你的实际群组用户名
👉 @your_channel  # 替换为你的实际频道用户名
```

### 3. 重启服务

```bash
python run.py
```

## ✅ 完成！

现在机器人会：
- ✅ 第一条消息自动发送群组邀请
- ✅ 自动识别iPhone型号、金额等信息
- ✅ 每2-3条消息提醒加入群组
- ✅ 自动推进贷款申请流程

## 📝 配置示例

完整配置示例请查看 `config_iphone_loan.yaml`

详细文档请查看 `IPHONE_LOAN_PROMPT_SETUP.md`


