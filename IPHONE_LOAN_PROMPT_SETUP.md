# iPhone Loan Telegram Bot - AI Prompt Configuration Guide

## 📋 Overview

This guide explains how to configure the AI prompt for the iPhone loan Telegram bot service in the Philippines. The system includes automatic recognition, auto-advancement, and traffic guidance features.

## 🚀 Quick Setup

### Step 1: Enable iPhone Loan Prompt

Edit `config.yaml` and add:

```yaml
ai_templates:
  prompt_type: "iphone_loan_telegram"
```

### Step 2: Configure Telegram Groups/Channels

The prompt includes placeholders `@your_group` and `@your_channel`. You need to:

1. **Option A**: Edit the prompt file directly
   - Open `src/ai/prompts/iphone_loan_telegram.py`
   - Replace `@your_group` with your actual Telegram group username
   - Replace `@your_channel` with your actual Telegram channel username

2. **Option B**: Use configuration file (recommended)
   - Add to `config.yaml`:
   ```yaml
   telegram_groups:
     main_group: "@your_actual_group"
     main_channel: "@your_actual_channel"
   ```

### Step 3: Restart Service

```bash
python run.py
```

## 📝 Prompt Features

### 🎯 Core Features

1. **Automatic Traffic Guidance**
   - First message always includes group/channel invitation
   - Reminds every 2-3 messages
   - Highest priority rule

2. **Auto-Recognition Logic**
   - Recognizes iPhone models (11-16)
   - Recognizes loan amounts (3,000-15,000 PHP)
   - Recognizes user information (storage, Apple ID, ID card)
   - Automatically advances conversation based on input

3. **Loan Business Rules**
   - Supported models: iPhone 11-16
   - Loan range: 3,000-15,000 PHP
   - Weekly fee: 12%
   - New customer discount: 50% first week
   - Late fee: 3% daily

### 🧠 Recognition Scenarios

#### Scenario 1: User Provides Model
**Input**: "iPhone 12 Pro"

**Bot Response**:
```
Received. I need the following information from you: Storage capacity, Apple ID status, ID card, desired loan amount.

If you haven't joined yet, please join our group first: @your_group
```

#### Scenario 2: User Provides Amount
**Input**: "Want to borrow 8,000"

**Bot Response**:
```
Application accepted. I need your iPhone model, storage capacity, Apple ID status, and ID card.

Processing can be done in just a few minutes.

Join the group to proceed: @your_group
```

#### Scenario 3: User Provides Model + Amount
**Bot Response**:
```
Your conditions look good. I still need: Storage capacity, Apple ID status, ID card.

Join our group for faster processing: @your_group
```

#### Scenario 4: User Provides Documents
**Bot Response**:
```
Information received. I'm preparing the application steps for you.

Please make sure to join our TG group for quick review: @your_group
```

#### Scenario 5: User Asks About Price/Interest
**Bot Response**:
```
First week 50% OFF, best deal if you apply now.

Example: Borrow 10,000 → Receive 9,400.

Join the group to get started: @your_group
```

#### Scenario 6: User Hesitates
**Bot Response**:
```
If you're ready to continue, I'm here to help anytime.

Join the group for faster processing: @your_group
```

## ⚙️ Configuration Options

### Basic Configuration

```yaml
ai_templates:
  prompt_type: "iphone_loan_telegram"
  processing: "Processing your request, please wait..."
  fallback: "I didn't fully understand. Could you describe your needs?"
```

### Advanced Configuration

```yaml
ai_templates:
  prompt_type: "iphone_loan_telegram"
  # Custom system prompt (optional, overrides default)
  system_prompt: |
    Your custom prompt here...

telegram_groups:
  main_group: "@your_group"
  main_channel: "@your_channel"

loan_config:
  supported_models:
    - "iPhone 11"
    - "iPhone 12"
    - "iPhone 13"
    - "iPhone 14"
    - "iPhone 15"
    - "iPhone 16"
  min_amount: 3000
  max_amount: 15000
  weekly_fee_percent: 12
  new_customer_discount: 50
  late_fee_percent: 3
```

## 🔧 Customization

### Customize Group/Channel Names

Edit `src/ai/prompts/iphone_loan_telegram.py`:

```python
IPHONE_LOAN_TELEGRAM_PROMPT = """...
👉 @your_actual_group_name
👉 @your_actual_channel_name
..."""
```

### Customize Loan Rules

Edit the prompt file to modify:
- Supported models
- Loan amounts
- Fee percentages
- Discount rates

### Customize Conversation Style

Modify the `CONVERSATION STYLE` section in the prompt file to change:
- Response length
- Tone
- Emoji usage
- Reminder frequency

## 📊 How It Works

1. **User sends first message** → Bot immediately sends group invitation
2. **User responds** → Bot recognizes intent (model, amount, etc.)
3. **Auto-advance** → Bot guides based on recognized information
4. **Remind group** → Every 2-3 messages, remind about joining
5. **Collect info** → Model, Amount, Storage, Apple ID, ID Card
6. **Final push** → Emphasize group benefits and urgency

## 🎯 Key Rules

1. **Traffic guidance is MANDATORY** in first message
2. **Remind about group** every 2-3 conversation rounds
3. **Auto-recognize** user input and advance accordingly
4. **Keep responses short** and action-oriented
5. **Always maintain** friendly, professional tone

## 🔍 Testing

### Test Recognition

Try these inputs to test auto-recognition:

1. "iPhone 13" → Should ask for storage, Apple ID, ID, amount
2. "8000" → Should ask for model, storage, Apple ID, ID
3. "iPhone 12 Pro, 8000" → Should ask for storage, Apple ID, ID
4. "128GB" → Should acknowledge and ask for remaining info
5. "How much interest?" → Should explain fees and remind about group

### Test Group Reminders

Have a conversation with 3-4 exchanges and verify that group invitation appears:
- In first message
- Every 2-3 messages after

## 📚 Files

- **Prompt File**: `src/ai/prompts/iphone_loan_telegram.py`
- **Template Manager**: `src/ai/prompt_templates.py`
- **Reply Generator**: `src/ai/reply_generator.py`
- **Config File**: `config.yaml`
- **Example Config**: `config_iphone_loan.yaml`

## ⚠️ Important Notes

1. **Group/Channel Names**: Must replace `@your_group` and `@your_channel` with actual usernames
2. **Language**: Prompt is in English, but bot can respond in user's language
3. **Restart Required**: Changes to prompt file require service restart
4. **Testing**: Always test with real conversations before going live

## 🆘 Troubleshooting

### Bot not sending group invitation?

- Check `prompt_type` is set to `"iphone_loan_telegram"` in config.yaml
- Verify prompt file is correctly imported
- Check logs for errors

### Recognition not working?

- Ensure prompt file is properly formatted
- Check that user input matches expected patterns
- Review conversation history in logs

### Group names not replaced?

- Edit `src/ai/prompts/iphone_loan_telegram.py` directly
- Or implement dynamic replacement in code

## 🎉 Next Steps

1. Configure your Telegram group/channel names
2. Test with sample conversations
3. Monitor bot responses and adjust as needed
4. Collect user feedback and optimize


