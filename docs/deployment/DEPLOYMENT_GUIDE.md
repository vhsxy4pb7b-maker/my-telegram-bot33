# 生产环境部署指南

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细部署步骤](#详细部署步骤)
- [配置说明](#配置说明)
- [数据库设置](#数据库设置)
- [服务启动](#服务启动)
- [验证和测试](#验证和测试)
- [生产环境优化](#生产环境优化)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

---

## 系统要求

### 硬件要求

- **CPU**: 2核心或以上
- **内存**: 4GB RAM 或以上
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求

- **操作系统**: 
  - Linux (Ubuntu 20.04+ / CentOS 7+)
  - Windows Server 2016+
  - macOS 10.15+
- **Python**: 3.9 或更高版本
- **PostgreSQL**: 12 或更高版本
- **Git**: 用于代码版本控制

### 必需的服务和API密钥

- ✅ Facebook App ID 和 App Secret
- ✅ Facebook Page Access Tokens (长期Token)
- ✅ OpenAI API Key
- ✅ Telegram Bot Token
- ✅ Telegram Chat ID (用于通知)

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/vhsxy4pb7b-maker/my-telegram-bot33.git
cd my-telegram-bot33
```

### 2. 创建虚拟环境

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp env.example .env
# 编辑 .env 文件，填入所有必需的配置
```

### 5. 配置业务规则

```bash
cp config/config.yaml.example config/config.yaml
# 编辑 config/config.yaml，配置业务规则
```

### 6. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

### 7. 启动服务

```bash
python run.py
```

服务将在 `http://localhost:8000` 启动。

---

## 详细部署步骤

### 步骤1: 环境准备

#### 1.1 安装Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
```

**CentOS/RHEL:**
```bash
sudo yum install python39 python39-pip
```

**macOS:**
```bash
brew install python@3.9
```

#### 1.2 安装PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### 1.3 创建数据库

```bash
sudo -u postgres psql
```

在PostgreSQL命令行中执行：
```sql
CREATE DATABASE facebook_customer_service;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE facebook_customer_service TO your_username;
\q
```

### 步骤2: 代码部署

#### 2.1 克隆代码

```bash
git clone https://github.com/vhsxy4pb7b-maker/my-telegram-bot33.git
cd my-telegram-bot33
git checkout main
```

#### 2.2 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

#### 2.3 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤3: 配置设置

#### 3.1 环境变量配置

创建 `.env` 文件：

```bash
cp env.example .env
nano .env  # 或使用你喜欢的编辑器
```

**必需的环境变量：**

```env
# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/facebook_customer_service
DATABASE_ECHO=false

# Facebook配置
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_user_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token

# OpenAI配置
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7

# Telegram配置
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=false

# 安全配置
SECRET_KEY=your_secret_key_here  # 使用: python -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM=HS256

# CORS配置（生产环境必需）
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### 3.2 业务规则配置

创建 `config/config.yaml`：

```bash
cp config/config.yaml.example config/config.yaml
nano config/config.yaml
```

**关键配置项：**

```yaml
# 自动回复配置
auto_reply:
  enabled: true
  default_language: "en"
  response_delay_seconds: 2

# Telegram群组配置
telegram_groups:
  main_group: https://t.me/+your_group_invite_link

# AI提示词配置
ai_templates:
  prompt_type: iphone_loan_telegram  # 或其他业务类型

# 页面设置（为每个页面单独配置）
page_settings:
  "your_page_id_1":
    auto_reply_enabled: true
    name: "业务页面1"
  "your_page_id_2":
    auto_reply_enabled: true
    name: "业务页面2"
```

### 步骤4: Facebook Token配置

#### 4.1 获取长期Token

使用提供的工具脚本：

```bash
python scripts/tools/convert_to_long_lived_token.py
```

或批量更新所有Token：

```bash
python scripts/tools/update_all_tokens_now.py
```

#### 4.2 配置页面Token

使用页面管理工具：

```bash
python scripts/tools/manage_pages.py
```

或直接编辑 `.page_tokens.json` 文件。

### 步骤5: 数据库初始化

#### 5.1 运行数据库迁移

```bash
# 检查当前迁移状态
alembic current

# 运行所有迁移
alembic upgrade head

# 验证迁移
alembic history
```

#### 5.2 验证数据库连接

```bash
python scripts/tools/verify_production_config.py
```

### 步骤6: 服务启动

#### 6.1 开发环境启动

```bash
python run.py
```

#### 6.2 生产环境启动（使用Gunicorn）

**安装Gunicorn:**
```bash
pip install gunicorn
```

**启动服务:**
```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info
```

#### 6.3 使用Systemd（Linux）

创建服务文件 `/etc/systemd/system/facebook-customer-service.service`:

```ini
[Unit]
Description=Facebook Customer Service API
After=network.target postgresql.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/my-telegram-bot33
Environment="PATH=/path/to/my-telegram-bot33/venv/bin"
ExecStart=/path/to/my-telegram-bot33/venv/bin/gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable facebook-customer-service
sudo systemctl start facebook-customer-service
sudo systemctl status facebook-customer-service
```

---

## 配置说明

### Facebook Webhook配置

1. **在Facebook Developer Console中配置Webhook:**
   - Webhook URL: `https://your-domain.com/webhook`
   - Verify Token: 使用 `.env` 中的 `FACEBOOK_VERIFY_TOKEN`
   - 订阅事件:
     - `messages` - 接收私信
     - `messaging_postbacks` - 接收按钮点击
     - `feed` - 接收评论（可选）

2. **验证Webhook:**
   ```bash
   curl -X GET "https://your-domain.com/webhook?hub.verify_token=YOUR_VERIFY_TOKEN&hub.challenge=CHALLENGE_STRING&hub.mode=subscribe"
   ```

### Telegram Bot配置

1. **创建Bot:**
   - 通过 @BotFather 创建新Bot
   - 获取Bot Token
   - 设置Webhook（如果需要）: `https://your-domain.com/telegram/webhook`

2. **获取Chat ID:**
   - 发送消息到你的Bot
   - 访问: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - 查找 `chat.id` 值

### OpenAI配置

1. **获取API Key:**
   - 访问 https://platform.openai.com/api-keys
   - 创建新的API Key
   - 确保账户有足够余额

2. **选择模型:**
   - 推荐: `gpt-4o-mini` (成本效益高)
   - 可选: `gpt-4`, `gpt-3.5-turbo`

---

## 数据库设置

### 数据库连接

确保 `DATABASE_URL` 格式正确：

```
postgresql://username:password@host:port/database_name
```

### 数据库迁移

**创建新迁移:**
```bash
alembic revision --autogenerate -m "描述信息"
```

**应用迁移:**
```bash
alembic upgrade head
```

**回滚迁移:**
```bash
alembic downgrade -1
```

### 数据库备份

**手动备份:**
```bash
pg_dump -U username facebook_customer_service > backup_$(date +%Y%m%d_%H%M%S).sql
```

**使用脚本备份:**
```bash
# Linux/macOS
bash scripts/backup_db.sh

# Windows
powershell scripts/backup_db.ps1
```

---

## 服务启动

### 开发模式

```bash
python run.py
```

### 生产模式（Gunicorn）

```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  --daemon
```

### Docker部署

**构建镜像:**
```bash
docker build -t facebook-customer-service .
```

**运行容器:**
```bash
docker run -d \
  --name facebook-customer-service \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  facebook-customer-service
```

---

## 验证和测试

### 1. 配置验证

```bash
python scripts/tools/verify_production_config.py
```

### 2. 核心功能测试

```bash
python scripts/tools/test_core_features.py
```

### 3. 健康检查

```bash
curl http://localhost:8000/health
```

预期响应：
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "uptime_seconds": 123.45
}
```

### 4. Webhook测试

**测试Facebook Webhook:**
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"object":"page","entry":[{"messaging":[{"sender":{"id":"123"},"message":{"text":"test"}}]}]}'
```

### 5. 端到端测试

1. 在Facebook页面发送测试消息
2. 检查日志确认消息已接收
3. 检查数据库确认消息已保存
4. 确认AI已回复
5. 检查Telegram通知（如果需要审核）

---

## 生产环境优化

### 1. 性能优化

**Gunicorn配置:**
- Workers数量: `(2 × CPU核心数) + 1`
- Worker类: `uvicorn.workers.UvicornWorker`
- Timeout: 120秒

**数据库优化:**
- 启用连接池
- 添加适当的索引
- 定期清理旧数据

### 2. 安全配置

**CORS设置:**
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**HTTPS配置:**
- 使用Nginx作为反向代理
- 配置SSL证书（Let's Encrypt）
- 启用HSTS

**防火墙规则:**
- 只开放必要端口（80, 443）
- 限制数据库访问（仅本地）

### 3. 日志配置

**日志轮转:**
- 最大文件大小: 10MB
- 保留备份数: 10个
- 日志级别: INFO（生产环境）

**日志位置:**
- 应用日志: `logs/app.log`
- 访问日志: `logs/access.log`
- 错误日志: `logs/error.log`

### 4. 监控配置

**健康检查端点:**
- URL: `/health`
- 检查频率: 每30秒
- 告警阈值: 连续3次失败

**资源监控:**
- CPU使用率
- 内存使用率
- 磁盘使用率
- 数据库连接数

---

## 监控和维护

### 1. 日志监控

**查看实时日志:**
```bash
tail -f logs/app.log
```

**查看错误日志:**
```bash
grep ERROR logs/app.log
```

### 2. 性能监控

**查看对话记录:**
```bash
python scripts/tools/view_complete_conversations.py
```

**查看对话序列:**
```bash
python scripts/tools/show_best_conversation_sequence.py
```

**诊断未回复消息:**
```bash
python scripts/tools/diagnose_unreplied_messages.py
```

### 3. Token管理

**检查Token过期:**
```bash
python scripts/tools/check_token_expiry.py
```

**更新Token:**
```bash
python scripts/tools/update_all_tokens_now.py
```

### 4. 数据库维护

**定期备份:**
- 每日自动备份
- 保留最近30天备份

**清理旧数据:**
```sql
-- 删除30天前的对话记录（谨慎使用）
DELETE FROM conversations 
WHERE created_at < NOW() - INTERVAL '30 days';
```

---

## 故障排除

### 常见问题

#### 1. 服务无法启动

**检查:**
- Python版本是否正确
- 依赖是否安装完整
- 环境变量是否配置
- 端口是否被占用

**解决:**
```bash
# 检查Python版本
python --version

# 重新安装依赖
pip install -r requirements.txt

# 检查端口占用
netstat -tulpn | grep 8000  # Linux
lsof -i :8000  # macOS
```

#### 2. 数据库连接失败

**检查:**
- 数据库服务是否运行
- 连接字符串是否正确
- 用户权限是否足够

**解决:**
```bash
# 检查PostgreSQL服务
sudo systemctl status postgresql

# 测试连接
psql -U username -d facebook_customer_service
```

#### 3. Facebook Webhook不接收消息

**检查:**
- Webhook URL是否正确
- Verify Token是否匹配
- 事件订阅是否启用
- 防火墙是否阻止

**解决:**
- 在Facebook Developer Console重新验证Webhook
- 检查服务器日志
- 测试Webhook端点

#### 4. AI不回复消息

**检查:**
- OpenAI API Key是否有效
- API余额是否充足
- 消息是否被过滤
- 自动回复是否启用

**解决:**
```bash
# 运行诊断工具
python scripts/tools/diagnose_unreplied_messages.py

# 检查配置
python scripts/tools/verify_production_config.py
```

#### 5. Token过期

**检查:**
```bash
python scripts/tools/check_token_expiry.py
```

**解决:**
```bash
python scripts/tools/update_all_tokens_now.py
```

### 日志分析

**查看最近的错误:**
```bash
tail -n 100 logs/app.log | grep ERROR
```

**统计错误类型:**
```bash
grep ERROR logs/app.log | awk '{print $NF}' | sort | uniq -c
```

### 性能问题

**检查系统资源:**
```bash
# CPU和内存
top

# 磁盘使用
df -h

# 网络连接
netstat -an | grep ESTABLISHED | wc -l
```

**数据库性能:**
```sql
-- 查看慢查询
SELECT * FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;
```

---

## 更新和升级

### 更新代码

```bash
# 拉取最新代码
git pull origin main

# 安装新依赖
pip install -r requirements.txt

# 运行数据库迁移
alembic upgrade head

# 重启服务
sudo systemctl restart facebook-customer-service
```

### 回滚

```bash
# 回滚到上一个版本
git checkout <previous_commit_hash>

# 回滚数据库迁移
alembic downgrade -1

# 重启服务
sudo systemctl restart facebook-customer-service
```

---

## 支持

### 获取帮助

- **GitHub Issues**: https://github.com/vhsxy4pb7b-maker/my-telegram-bot33/issues
- **文档**: 查看 `docs/` 目录
- **工具脚本**: 查看 `scripts/tools/` 目录

### 有用的工具

- `verify_production_config.py` - 验证配置
- `test_core_features.py` - 测试核心功能
- `diagnose_unreplied_messages.py` - 诊断未回复消息
- `check_token_expiry.py` - 检查Token过期
- `view_complete_conversations.py` - 查看对话记录

---

## 附录

### A. 环境变量完整列表

参考 `env.example` 文件获取所有可用的环境变量。

### B. 配置文件说明

参考 `config/config.yaml.example` 了解所有配置选项。

### C. API文档

启动服务后访问:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### D. 数据库模型

查看 `src/database/models.py` 了解数据库结构。

---

**最后更新**: 2025-12-13  
**版本**: 2.0.0

