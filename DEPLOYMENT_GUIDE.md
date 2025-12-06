# 部署指南

## 📋 目录

1. [环境准备](#环境准备)
2. [开发环境部署](#开发环境部署)
3. [生产环境部署](#生产环境部署)
4. [Docker 部署](#docker-部署)
5. [系统服务部署](#系统服务部署)
6. [Nginx 反向代理](#nginx-反向代理)
7. [监控和维护](#监控和维护)
8. [故障排查](#故障排查)

---

## 环境准备

### 系统要求

- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 7+), Windows, macOS
- **Python**: 3.9 或更高版本
- **数据库**: PostgreSQL 12 或更高版本
- **内存**: 最低 2GB，推荐 4GB+
- **磁盘**: 最低 10GB 可用空间

### 必需软件

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv postgresql postgresql-contrib git

# CentOS/RHEL
sudo yum install -y python3 python3-pip postgresql postgresql-server git

# macOS
brew install python3 postgresql git

# Windows
# 下载并安装 Python 3.9+ 和 PostgreSQL
```

---

## 开发环境部署

### 步骤 1: 克隆项目

```bash
git clone <your-repo-url>
cd 无极1
```

### 步骤 2: 创建虚拟环境

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 步骤 3: 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 4: 配置环境变量

创建 `.env` 文件：

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/facebook_customer_service

# Facebook 配置
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token

# OpenAI 配置
OPENAI_API_KEY=your_openai_key

# Telegram 配置
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# 应用配置
SECRET_KEY=your_secret_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Instagram 配置（可选）
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_USER_ID=your_instagram_user_id

# 第三方集成（可选）
MANYCHAT_API_KEY=your_manychat_key
BOTCAKE_API_KEY=your_botcake_key
```

### 步骤 5: 创建数据库

```bash
# 登录 PostgreSQL
sudo -u postgres psql

# 创建数据库
CREATE DATABASE facebook_customer_service;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE facebook_customer_service TO your_user;
\q
```

### 步骤 6: 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head

# 或直接创建表（如果 Alembic 不可用）
python -c "from src.database.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 步骤 7: 配置业务规则

复制配置文件：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml` 配置业务规则。

### 步骤 8: 启动服务

```bash
# 方式 1: 使用启动脚本
python run.py

# 方式 2: 直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 步骤 9: 验证部署

访问以下 URL 验证：

- 健康检查: http://localhost:8000/health
- API 文档: http://localhost:8000/docs
- 统计接口: http://localhost:8000/statistics/daily

---

## 生产环境部署

### 方式 1: Docker 部署（推荐）

#### 创建 Dockerfile

已存在 `Dockerfile`，直接使用：

```bash
# 构建镜像
docker build -t customer-service:latest .

# 运行容器
docker run -d \
  --name customer-service \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/config.yaml:/app/config.yaml \
  customer-service:latest
```

#### 使用 Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: facebook_customer_service
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./config.yaml:/app/config.yaml
    depends_on:
      - db
    restart: unless-stopped

volumes:
  postgres_data:
```

启动服务：

```bash
docker-compose up -d
```

### 方式 2: 系统服务部署

#### 创建 systemd 服务文件

创建 `/etc/systemd/system/customer-service.service`:

```ini
[Unit]
Description=Customer Service API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/customer-service
Environment="PATH=/opt/customer-service/venv/bin"
ExecStart=/opt/customer-service/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start customer-service

# 设置开机自启
sudo systemctl enable customer-service

# 查看状态
sudo systemctl status customer-service

# 查看日志
sudo journalctl -u customer-service -f
```

### 方式 3: 使用 Gunicorn + Uvicorn Workers

安装 Gunicorn：

```bash
pip install gunicorn
```

创建 `gunicorn_config.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
```

启动服务：

```bash
gunicorn src.main:app -c gunicorn_config.py
```

---

## Nginx 反向代理

### 安装 Nginx

```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 配置 Nginx

创建 `/etc/nginx/sites-available/customer-service`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 重定向到 HTTPS（可选）
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件（如果有）
    location /static/ {
        alias /opt/customer-service/static/;
        expires 30d;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/customer-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL 证书（Let's Encrypt）

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 监控和维护

### 日志管理

#### 应用日志

日志文件位置：
- 开发环境: 控制台输出
- 生产环境: `/var/log/customer-service/`

配置日志轮转，创建 `/etc/logrotate.d/customer-service`:

```
/var/log/customer-service/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload customer-service > /dev/null 2>&1 || true
    endscript
}
```

### 健康检查

定期检查服务健康状态：

```bash
# 健康检查脚本
#!/bin/bash
curl -f http://localhost:8000/health || exit 1
```

添加到 cron：

```bash
# 每5分钟检查一次
*/5 * * * * /opt/customer-service/health_check.sh
```

### 数据库备份

创建备份脚本 `backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U user facebook_customer_service > "$BACKUP_DIR/backup_$DATE.sql"
# 保留最近30天的备份
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

添加到 cron：

```bash
# 每天凌晨2点备份
0 2 * * * /opt/customer-service/backup_db.sh
```

### 性能监控

使用工具监控系统性能：

- **htop**: 系统资源监控
- **pg_stat_statements**: PostgreSQL 性能监控
- **Prometheus + Grafana**: 指标收集和可视化（可选）

---

## 故障排查

### 常见问题

#### 1. 服务无法启动

```bash
# 检查端口是否被占用
sudo netstat -tulpn | grep 8000

# 检查日志
sudo journalctl -u customer-service -n 50

# 检查配置
python -c "from src.config import settings; print('OK')"
```

#### 2. 数据库连接失败

```bash
# 测试数据库连接
psql -h localhost -U user -d facebook_customer_service

# 检查 PostgreSQL 服务
sudo systemctl status postgresql

# 检查防火墙
sudo ufw status
```

#### 3. API 密钥错误

```bash
# 验证配置
python -c "from src.config import settings; print(settings.facebook_app_id)"
```

#### 4. 内存不足

```bash
# 检查内存使用
free -h

# 调整 Gunicorn workers
# 在 gunicorn_config.py 中减少 workers 数量
```

### 调试模式

开发环境启用调试：

```bash
# .env 文件
DEBUG=True

# 查看详细日志
uvicorn src.main:app --log-level debug
```

---

## 部署检查清单

### 部署前

- [ ] 所有环境变量已配置
- [ ] 数据库已创建并初始化
- [ ] 配置文件已设置
- [ ] 依赖已安装
- [ ] 测试环境验证通过

### 部署后

- [ ] 服务正常启动
- [ ] 健康检查通过
- [ ] API 文档可访问
- [ ] 数据库连接正常
- [ ] Webhook 配置正确
- [ ] 日志正常输出
- [ ] 监控已设置

### 生产环境

- [ ] 使用 HTTPS
- [ ] 防火墙已配置
- [ ] 日志轮转已设置
- [ ] 数据库备份已配置
- [ ] 监控告警已设置
- [ ] 系统服务已配置
- [ ] 反向代理已配置

---

## 快速部署脚本

创建 `deploy.sh`:

```bash
#!/bin/bash
set -e

echo "开始部署..."

# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行数据库迁移
alembic upgrade head

# 4. 重启服务
sudo systemctl restart customer-service

# 5. 检查服务状态
sleep 5
sudo systemctl status customer-service

echo "部署完成！"
```

使用：

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 相关文档

- [快速开始指南](QUICKSTART.md)
- [配置指南](CONFIGURE_AI_REPLY.md)
- [统计数据指南](STATISTICS_GUIDE.md)
- [API 文档](http://localhost:8000/docs)

---

## 获取帮助

如遇问题，请：
1. 查看日志文件
2. 检查配置是否正确
3. 参考故障排查章节
4. 查看相关文档
