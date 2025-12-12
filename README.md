# Facebook 客服自动化系统

一个完整的从 Facebook 到 Telegram Bot 的自动化客服系统，支持 AI 自动回复、资料收集、智能过滤和人工审核。

## 系统架构

```
Facebook（广告 & 私信 & 评论）
      ↓ 自动回复
AI 智能客服（ManyChat / Botcake）
      ↓ 自动收集资料 + 自动过滤
Telegram Bot（团队的内部系统）
      ↓
人工审核 / AI 辅助判断
```

## 功能特性

- ✅ **Facebook 消息接收**: 支持广告、私信、评论等多种消息类型
- ✅ **AI 自动回复**: 集成 OpenAI API，智能生成回复
- ✅ **资料自动收集**: 自动提取客户信息（姓名、邮箱、电话等）
- ✅ **智能过滤**: 关键词过滤、情感分析、优先级判断
- ✅ **Telegram 通知**: 自动发送审核通知到团队 Telegram
- ✅ **人工审核**: 支持通过 Telegram Bot 进行审核操作
- ✅ **第三方集成**: 支持 ManyChat 和 Botcake 集成

## 技术栈

- **后端框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **数据库迁移**: Alembic
- **AI 服务**: OpenAI API
- **消息平台**: Facebook Graph API, Telegram Bot API
- **第三方集成**: ManyChat API, Botcake API

## 快速开始

### 1. 环境要求

- Python 3.9+
- PostgreSQL 12+
- 所有 API 密钥（Facebook, OpenAI, Telegram 等）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填写相关配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下信息：

- `DATABASE_URL`: PostgreSQL 数据库连接字符串
- `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`, `FACEBOOK_ACCESS_TOKEN`: Facebook API 配置
- `OPENAI_API_KEY`: OpenAI API 密钥
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`: Telegram Bot 配置
- 其他可选配置（ManyChat, Botcake 等）

### 4. 配置业务规则

复制 `config/config.yaml.example` 为 `config/config.yaml` 并自定义配置：

```bash
cp config/config.yaml.example config/config.yaml
```

在 `config/config.yaml` 中配置：
- 自动回复模板
- 资料收集字段
- 过滤规则
- 优先级规则

### 5. 初始化数据库

```bash
# 创建数据库迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 6. 启动服务

```bash
python -m src.main
```

或使用 uvicorn：

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

服务将在 `http://localhost:8000` 启动。

### 7. 配置 Facebook Webhook

1. 在 Facebook Developer Console 中配置 Webhook URL: `https://your-domain.com/webhook`
2. 验证令牌设置为 `.env` 中的 `FACEBOOK_VERIFY_TOKEN`
3. 订阅以下事件：
   - `messages`
   - `messaging_postbacks`
   - `feed` (用于评论)

### 8. 配置 Telegram Bot

1. 创建 Telegram Bot（通过 @BotFather）
2. 获取 Bot Token 并填入 `.env`
3. 设置 Webhook URL: `https://your-domain.com/telegram/webhook`

## API 文档

启动服务后，访问以下地址查看 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 项目文档

项目文档已整理到 `docs/` 目录，按类别分类：

- **[文档索引](docs/README.md)** - 查看所有文档的完整索引
- **部署文档** - 查看 [docs/deployment/](docs/deployment/) 了解部署指南
- **功能指南** - 查看 [docs/guides/](docs/guides/) 了解功能使用方法
- **架构文档** - 查看 [docs/architecture/](docs/architecture/) 了解系统架构

## 🛠️ 工具脚本

项目提供了多个工具脚本，位于 `scripts/` 目录：

### 环境设置脚本 (scripts/setup/)
- `activate_venv.ps1` - 激活虚拟环境（Windows PowerShell）

### 工具脚本 (scripts/tools/)
- `check_facebook_permissions.py` - 检查 Facebook 权限
- `exchange_token.py` - 交换 Token

### 部署脚本 (scripts/deployment/)
- `deploy.bat` - Windows 部署脚本
- `deploy.sh` - Linux/Mac 部署脚本

### 备份脚本 (scripts/backup/)
- `backup_db.ps1` - Windows 数据库备份脚本
- `backup_db.sh` - Linux/Mac 数据库备份脚本

## 项目结构

```
project/
├── src/
│   ├── facebook/          # Facebook 集成模块
│   │   ├── api_client.py      # Facebook API 客户端
│   │   ├── message_parser.py  # 消息解析器
│   │   └── webhook_handler.py # Webhook 处理器
│   ├── ai/                # AI 模块
│   │   ├── conversation_manager.py  # 对话管理
│   │   ├── prompt_templates.py      # 提示词模板
│   │   └── reply_generator.py       # 回复生成器
│   ├── collector/         # 资料收集与过滤
│   │   ├── data_collector.py   # 资料收集
│   │   ├── data_validator.py   # 数据验证
│   │   └── filter_engine.py    # 过滤引擎
│   ├── integrations/      # 第三方集成
│   │   ├── manychat_client.py      # ManyChat 客户端
│   │   ├── botcake_client.py       # Botcake 客户端
│   │   └── integration_manager.py  # 集成管理器
│   ├── telegram/          # Telegram Bot
│   │   ├── bot_handler.py         # Bot 处理器
│   │   ├── command_processor.py   # 命令处理
│   │   └── notification_sender.py # 通知发送
│   ├── database/          # 数据库
│   │   ├── database.py    # 数据库连接
│   │   └── models.py      # 数据模型
│   ├── config.py          # 配置管理
│   ├── main.py            # 主应用入口
│   └── main_processor.py  # 消息处理流程
├── alembic/               # 数据库迁移
├── tests/                 # 测试文件
├── config/               # 配置文件目录
│   ├── config.yaml.example   # 配置文件示例
│   └── ...
├── docs/                 # 文档目录
│   ├── deployment/       # 部署文档
│   ├── guides/          # 功能指南
│   ├── architecture/    # 架构文档
│   └── reports/         # 报告文档
├── scripts/              # 脚本目录
│   ├── setup/          # 环境设置脚本
│   ├── tools/          # 工具脚本
│   └── deployment/     # 部署脚本
├── data/                # 数据文件目录
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
└── README.md            # 项目文档
```

## 数据流程

1. **接收消息**: Facebook Webhook 接收消息事件
2. **解析消息**: 解析消息类型和内容
3. **保存对话**: 保存到数据库
4. **AI 回复**: 生成并发送 AI 回复
5. **资料收集**: 提取客户信息
6. **过滤判断**: 应用过滤规则
7. **Telegram 通知**: 发送审核通知
8. **人工审核**: 通过 Telegram Bot 进行审核

## 使用示例

### Telegram 审核命令

- `/approve_{conversation_id}` - 通过审核
- `/reject_{conversation_id}` - 拒绝审核
- `/review_{conversation_id}` - 查看详情

### 自定义过滤规则

在 `config/config.yaml` 中配置：

```yaml
filtering:
  keyword_filter:
    enabled: true
    spam_keywords: ["垃圾", "广告"]
    block_keywords: ["诈骗", "scam"]
  
  priority_rules:
    - condition: "包含紧急关键词"
      keywords: ["紧急", "urgent"]
      priority: "high"
```

## 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/
isort src/
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

如有问题，请提交 Issue 或联系开发团队。


