# 服务器部署指南

## 📋 目录

1. [服务器准备](#服务器准备)
2. [Docker 部署（推荐）](#docker-部署推荐)
3. [系统服务部署](#系统服务部署)
4. [Nginx 反向代理](#nginx-反向代理)
5. [SSL 证书配置](#ssl-证书配置)
6. [监控和维护](#监控和维护)

---

## 服务器准备

### 系统要求

- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / Debian 11+
- **CPU**: 2 核或以上
- **内存**: 4GB 或以上
- **磁盘**: 20GB 或以上可用空间
- **网络**: 公网 IP，开放 80/443 端口

### 初始设置

```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 安装基础工具
sudo apt-get install -y curl wget git vim

# 安装 Docker（如果使用 Docker 部署）
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装 PostgreSQL（如果不使用 Docker）
sudo apt-get install -y postgresql postgresql-contrib
```

---

## Docker 部署（推荐）

### 步骤 1: 上传项目文件

```bash
# 方式 1: 使用 Git
git clone <your-repo-url>
cd 无极1

# 方式 2: 使用 SCP 上传
# 在本地执行：
# scp -r . user@your-server:/opt/customer-service/
```

### 步骤 2: 配置环境变量

```bash
# 在服务器上创建 .env 文件
cd /opt/customer-service
nano .env
```

填入所有必需的配置（参考 `env.example`）

### 步骤 3: 配置业务规则

```bash
# 创建配置文件
cp config.yaml.example config.yaml
nano config.yaml
```

### 步骤 4: 启动服务

```bash
# 启动所有服务（数据库 + 应用）
docker-compose up -d

# 查看日志
docker-compose logs -f app

# 查看服务状态
docker-compose ps
```

### 步骤 5: 验证部署

```bash
# 健康检查
curl http://localhost:8000/health

# 查看容器日志
docker-compose logs app
```

---

## 系统服务部署

如果不使用 Docker，可以使用 systemd 服务。

### 步骤 1: 安装 Python 和依赖

```bash
# 安装 Python 3.9+
sudo apt-get install -y python3 python3-pip python3-venv

# 创建应用目录
sudo mkdir -p /opt/customer-service
cd /opt/customer-service

# 上传项目文件（使用 Git 或 SCP）
git clone <your-repo-url> .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 2: 配置环境变量

```bash
# 创建 .env 文件
nano .env
```

### 步骤 3: 配置数据库

```bash
# 创建数据库
sudo -u postgres psql
CREATE DATABASE facebook_customer_service;
CREATE USER customer_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE facebook_customer_service TO customer_user;
\q

# 运行数据库迁移
source venv/bin/activate
alembic upgrade head
```

### 步骤 4: 创建 systemd 服务

创建 `/etc/systemd/system/customer-service.service`:

```ini
[Unit]
Description=Customer Service API
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/customer-service
Environment="PATH=/opt/customer-service/venv/bin"
EnvironmentFile=/opt/customer-service/.env
ExecStart=/opt/customer-service/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=customer-service

# 安全设置
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 步骤 5: 启动服务

```bash
# 设置权限
sudo chown -R www-data:www-data /opt/customer-service

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

---

## Nginx 反向代理

### 安装 Nginx

```bash
sudo apt-get install -y nginx
```

### 配置 Nginx

创建 `/etc/nginx/sites-available/customer-service`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 日志
    access_log /var/log/nginx/customer-service-access.log;
    error_log /var/log/nginx/customer-service-error.log;

    # 客户端最大请求体大小
    client_max_body_size 10M;

    # API 路由
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 健康检查（可选）
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
```

### 启用配置

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/customer-service /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

---

## SSL 证书配置

### 使用 Let's Encrypt（免费）

```bash
# 安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

### 手动配置 SSL

编辑 Nginx 配置：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... 其他配置
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 监控和维护

### 日志管理

#### 应用日志

```bash
# systemd 服务日志
sudo journalctl -u customer-service -f

# Docker 日志
docker-compose logs -f app
```

#### 日志轮转

创建 `/etc/logrotate.d/customer-service`:

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

### 健康检查脚本

创建 `/opt/customer-service/health_check.sh`:

```bash
#!/bin/bash
URL="http://localhost:8000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ Service is healthy"
    exit 0
else
    echo "❌ Service is unhealthy (HTTP $RESPONSE)"
    # 可以添加重启服务的逻辑
    # systemctl restart customer-service
    exit 1
fi
```

添加到 cron:

```bash
# 每5分钟检查一次
*/5 * * * * /opt/customer-service/health_check.sh
```

### 数据库备份

创建 `/opt/customer-service/backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="facebook_customer_service"
DB_USER="customer_user"

mkdir -p $BACKUP_DIR

# 备份数据库
PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USER -h localhost $DB_NAME > "$BACKUP_DIR/backup_$DATE.sql"

# 压缩备份
gzip "$BACKUP_DIR/backup_$DATE.sql"

# 保留最近30天的备份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

添加到 cron:

```bash
# 每天凌晨2点备份
0 2 * * * /opt/customer-service/backup_db.sh
```

---

## 防火墙配置

### UFW（Ubuntu）

```bash
# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

### firewalld（CentOS）

```bash
# 允许 HTTP/HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 云服务器部署

### 阿里云 / 腾讯云

1. **购买服务器**
   - 选择 Ubuntu 20.04+ 系统
   - 配置：2核4GB 或以上

2. **安全组配置**
   - 开放 22 端口（SSH）
   - 开放 80 端口（HTTP）
   - 开放 443 端口（HTTPS）

3. **域名解析**
   - 将域名 A 记录指向服务器 IP

4. **按照上述步骤部署**

### AWS EC2

```bash
# 连接到 EC2 实例
ssh -i your-key.pem ubuntu@your-ec2-ip

# 按照上述步骤部署
```

---

## 部署检查清单

### 部署前
- [ ] 服务器已准备（系统、内存、磁盘）
- [ ] 域名已解析到服务器 IP
- [ ] 防火墙已配置
- [ ] SSH 密钥已配置

### 部署中
- [ ] 项目文件已上传
- [ ] 环境变量已配置
- [ ] 数据库已创建
- [ ] 服务已启动

### 部署后
- [ ] 健康检查通过
- [ ] API 文档可访问
- [ ] Webhook 配置正确
- [ ] SSL 证书已配置
- [ ] 监控已设置

---

## 常用命令

```bash
# Docker 部署
docker-compose up -d              # 启动服务
docker-compose down               # 停止服务
docker-compose logs -f app        # 查看日志
docker-compose restart app        # 重启服务
docker-compose ps                 # 查看状态

# systemd 服务
sudo systemctl start customer-service      # 启动
sudo systemctl stop customer-service       # 停止
sudo systemctl restart customer-service    # 重启
sudo systemctl status customer-service    # 状态
sudo journalctl -u customer-service -f    # 日志

# Nginx
sudo nginx -t                     # 测试配置
sudo systemctl reload nginx       # 重载配置
sudo systemctl restart nginx      # 重启

# 数据库
alembic upgrade head              # 升级数据库
alembic downgrade -1              # 回退版本
```

---

## 故障排查

### 服务无法启动

```bash
# 检查日志
sudo journalctl -u customer-service -n 50

# 检查配置
python3 -c "from src.config import settings; print('OK')"

# 检查端口
sudo netstat -tulpn | grep 8000
```

### 数据库连接失败

```bash
# 测试连接
psql -h localhost -U customer_user -d facebook_customer_service

# 检查 PostgreSQL 服务
sudo systemctl status postgresql
```

### Nginx 502 错误

```bash
# 检查应用是否运行
curl http://localhost:8000/health

# 检查 Nginx 错误日志
sudo tail -f /var/log/nginx/customer-service-error.log
```

---

## 相关文档

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 完整部署指南
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - 快速部署
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 部署检查清单


