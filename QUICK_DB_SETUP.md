# 快速数据库设置指南

## 情况 1: 已安装 PostgreSQL

如果您已经安装了 PostgreSQL，运行：
```bash
python setup_database.py
```

然后输入：
- **主机**: 通常是 `localhost`（直接按回车使用默认值）
- **端口**: 通常是 `5432`（直接按回车使用默认值）
- **用户名**: 通常是 `postgres`（直接按回车使用默认值）
- **密码**: 输入安装 PostgreSQL 时设置的 postgres 用户密码

脚本会自动：
1. 测试连接
2. 创建数据库 `facebook_customer_service`
3. 生成 DATABASE_URL 并提示您添加到 .env 文件

## 情况 2: 未安装 PostgreSQL

### 选项 A: 安装 PostgreSQL（推荐用于生产环境）

1. **下载安装程序**
   - 访问：https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   - 选择 Windows 版本下载

2. **运行安装程序**
   - 选择安装路径（默认即可）
   - **重要**: 记住设置的 postgres 用户密码
   - 端口使用默认 5432
   - 完成安装

3. **验证安装**
   - 打开服务管理器，查找 PostgreSQL 服务
   - 确保服务正在运行

4. **创建数据库**
   - 运行：`python setup_database.py`

### 选项 B: 使用 SQLite（仅用于测试）

如果暂时不想安装 PostgreSQL，可以修改配置使用 SQLite：

1. **修改 .env 文件**
   将 `DATABASE_URL` 改为：
   ```
   DATABASE_URL=sqlite:///./facebook_customer_service.db
   ```

2. **注意**: SQLite 有一些限制，生产环境建议使用 PostgreSQL

## 情况 3: 使用 Docker（如果有 Docker）

```bash
# 启动 PostgreSQL 容器
docker run --name postgres-fb-cs -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=facebook_customer_service -p 5432:5432 -d postgres

# 然后运行
python setup_database.py
# 输入: localhost, 5432, postgres, your_password
```

## 手动创建数据库

如果脚本无法使用，可以手动创建：

### 使用 psql 命令行

```bash
# 连接到 PostgreSQL
psql -U postgres

# 在 psql 中执行
CREATE DATABASE facebook_customer_service;

# 退出
\q
```

### 使用 pgAdmin（图形界面）

1. 打开 pgAdmin
2. 连接到服务器
3. 右键 Databases → Create → Database
4. 名称：`facebook_customer_service`
5. 保存

## 配置 .env 文件

数据库创建后，在 `.env` 文件中设置：

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/facebook_customer_service
```

替换 `your_password` 为实际的 postgres 用户密码。

## 验证数据库连接

运行验证脚本：
```bash
python verify_setup.py
```

如果看到 "✓ 数据库连接成功"，说明配置正确。

## 下一步

数据库配置完成后：
```bash
# 初始化数据库表
alembic upgrade head

# 或使用 SQLAlchemy 直接创建
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

