# PostgreSQL 数据库设置指南

## 安装 PostgreSQL

### Windows 安装

1. **下载 PostgreSQL**
   - 访问：https://www.postgresql.org/download/windows/
   - 下载 PostgreSQL 安装程序
   - 或使用 EnterpriseDB 的安装程序：https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. **运行安装程序**
   - 选择安装路径（默认：`C:\Program Files\PostgreSQL\版本号`）
   - 设置超级用户（postgres）密码（**请记住这个密码！**）
   - 选择端口（默认：5432）
   - 选择区域设置（建议：Chinese, China）

3. **完成安装**
   - 安装完成后，确保 PostgreSQL 服务正在运行

### 验证安装

打开命令提示符或 PowerShell，运行：
```bash
psql --version
```

如果显示版本号，说明安装成功。

## 创建数据库

### 方法 1：使用 psql 命令行

1. **连接到 PostgreSQL**
   ```bash
   psql -U postgres
   ```
   输入安装时设置的 postgres 用户密码

2. **创建数据库**
   ```sql
   CREATE DATABASE facebook_customer_service;
   ```

3. **验证创建**
   ```sql
   \l
   ```
   应该能看到 `facebook_customer_service` 数据库

4. **退出**
   ```sql
   \q
   ```

### 方法 2：使用 pgAdmin（图形界面）

1. **打开 pgAdmin**
   - 从开始菜单启动 pgAdmin

2. **连接到服务器**
   - 右键点击 "Servers" → "Create" → "Server"
   - 输入连接信息（主机：localhost，端口：5432，用户名：postgres）

3. **创建数据库**
   - 右键点击 "Databases" → "Create" → "Database"
   - 名称：`facebook_customer_service`
   - 点击 "Save"

### 方法 3：使用 Python 脚本

创建并运行以下脚本：

```python
import psycopg2
from psycopg2 import sql

# 连接到默认的 postgres 数据库
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="your_password",  # 替换为您的密码
    database="postgres"
)

conn.autocommit = True
cursor = conn.cursor()

# 创建数据库
try:
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier("facebook_customer_service")
        )
    )
    print("✓ 数据库创建成功！")
except psycopg2.errors.DuplicateDatabase:
    print("数据库已存在")
finally:
    cursor.close()
    conn.close()
```

## 配置 .env 文件

在 `.env` 文件中设置数据库连接字符串：

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/facebook_customer_service
```

**格式说明：**
- `postgresql://` - 协议
- `postgres` - 用户名
- `your_password` - 密码（替换为实际密码）
- `localhost` - 主机
- `5432` - 端口
- `facebook_customer_service` - 数据库名

## 初始化数据库表

数据库创建后，运行迁移创建表结构：

```bash
# 方法 1：使用 Alembic
alembic upgrade head

# 方法 2：直接使用 SQLAlchemy
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 验证数据库连接

运行验证脚本：
```bash
python verify_setup.py
```

如果数据库连接成功，会看到：
```
✓ 数据库连接成功
```

## 常见问题

### 问题 1：连接被拒绝
**错误：** `Connection refused`

**解决方案：**
- 检查 PostgreSQL 服务是否运行
- Windows: 服务管理器 → 查找 "postgresql" 服务 → 启动
- 或运行：`net start postgresql-x64-版本号`

### 问题 2：认证失败
**错误：** `password authentication failed`

**解决方案：**
- 检查 `.env` 中的密码是否正确
- 确认用户名是否正确（默认：postgres）

### 问题 3：数据库不存在
**错误：** `database "facebook_customer_service" does not exist`

**解决方案：**
- 按照上述步骤创建数据库
- 检查数据库名称拼写

### 问题 4：端口被占用
**错误：** `port 5432 is already in use`

**解决方案：**
- 检查是否有其他 PostgreSQL 实例运行
- 或更改端口号（需要同时更新 `.env` 中的端口）

## 下一步

数据库配置完成后：
1. 运行数据库迁移：`alembic upgrade head`
2. 验证连接：`python verify_setup.py`
3. 启动服务：`python run.py`

