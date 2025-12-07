# 服务器快速部署指南

## 🚀 5分钟快速部署到服务器

### 前提条件

- Linux 服务器（Ubuntu 20.04+ 推荐）
- 已安装 Docker 和 Docker Compose
- 域名已解析到服务器 IP

### 步骤 1: 连接服务器

```bash
ssh user@your-server-ip
```

### 步骤 2: 克隆或上传项目

```bash
# 方式 1: 使用 Git
git clone <your-repo-url>
cd 无极1

# 方式 2: 使用 SCP（在本地执行）
# scp -r . user@your-server:/opt/customer-service/
```

### 步骤 3: 配置环境变量

```bash
# 创建 .env 文件
nano .env
```

填入所有必需的配置（参考 `env.example`）

### 步骤 4: 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

### 步骤 5: 配置 Nginx（可选）

```bash
# 安装 Nginx
sudo apt-get install -y nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/customer-service
```

粘贴以下配置（修改域名）：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/customer-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 步骤 6: 配置 SSL（可选）

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## ✅ 验证部署

```bash
# 健康检查
curl http://localhost:8000/health

# 或通过域名
curl http://your-domain.com/health
```

## 📝 必需配置

在 `.env` 文件中必须配置：

```env
DATABASE_URL=postgresql://user:password@db:5432/facebook_customer_service
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
OPENAI_API_KEY=your_openai_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
SECRET_KEY=your_secret_key
```

## 🔧 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app

# 重启服务
docker-compose restart app

# 停止服务
docker-compose down

# 更新代码后重启
git pull
docker-compose up -d --build
```

## 📚 详细文档

完整服务器部署指南请查看 [SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)


