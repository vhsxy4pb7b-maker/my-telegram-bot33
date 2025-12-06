# 🚀 从这里开始

欢迎使用 Facebook 客服自动化系统！按照以下步骤快速开始。

## 快速开始（5 分钟）

### 第 1 步：安装依赖

```bash
python -m pip install -r requirements.txt
```

### 第 2 步：配置环境变量

1. 打开 `.env` 文件
2. 参考 `API_KEYS_GUIDE.md` 获取所有 API 密钥
3. 填入所有必需的配置项

**最低必需配置：**
- `DATABASE_URL` - PostgreSQL 数据库连接
- `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`, `FACEBOOK_ACCESS_TOKEN`, `FACEBOOK_VERIFY_TOKEN`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- `SECRET_KEY`

### 第 3 步：创建数据库

```sql
-- 在 PostgreSQL 中执行
CREATE DATABASE facebook_customer_service;
```

### 第 4 步：初始化数据库

```bash
# 方法 1：使用 Alembic（推荐）
alembic upgrade head

# 方法 2：直接创建表（如果 Alembic 不可用）
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 第 5 步：启动服务

```bash
python run.py
```

访问 http://localhost:8000/docs 查看 API 文档！

---

## 📚 详细文档

- **`CHECKLIST.md`** - 完整的配置检查清单
- **`API_KEYS_GUIDE.md`** - 详细的 API 密钥获取指南
- **`SETUP_INSTRUCTIONS.md`** - 详细的设置说明
- **`README.md`** - 完整的项目文档和架构说明
- **`QUICKSTART.md`** - 快速启动指南

---

## 🆘 遇到问题？

1. **检查配置清单** - 查看 `CHECKLIST.md` 确保所有步骤都完成
2. **查看日志** - 启动服务时查看控制台输出的错误信息
3. **验证配置** - 运行 `python -c "from src.config import settings; print('OK')"` 测试配置

---

## ✅ 验证安装

运行以下命令验证一切正常：

```bash
# 1. 测试配置
python -c "from src.config import settings; print('✓ 配置加载成功')"

# 2. 测试数据库
python -c "from src.database.database import engine; engine.connect(); print('✓ 数据库连接成功')"

# 3. 启动服务
python run.py
```

然后访问：
- http://localhost:8000/health - 应该返回 `{"status": "healthy"}`
- http://localhost:8000/docs - 查看 API 文档

---

祝您使用愉快！🎉


