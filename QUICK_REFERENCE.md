# 快速参考卡片

## 🚀 系统访问

### API 文档
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 系统端点
- **系统信息**: http://localhost:8000/
- **健康检查**: http://localhost:8000/health

---

## 📋 常用命令

### 启动服务
```bash
python run.py
```

### 停止服务
- 按 `Ctrl+C` 或关闭终端

### 验证配置
```bash
python verify_setup.py
```

### 测试 API
```bash
python test_api.py
```

### 配置 API 密钥
```bash
python configure_api_keys.py
```

---

## 🔑 API 密钥配置

### 必需配置（完整功能）
1. **Facebook API**
   - `FACEBOOK_APP_ID`
   - `FACEBOOK_APP_SECRET`
   - `FACEBOOK_ACCESS_TOKEN`
   - `FACEBOOK_VERIFY_TOKEN`

2. **OpenAI API**
   - `OPENAI_API_KEY`

3. **Telegram Bot**
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### 获取方式
- 查看 `API_KEYS_GUIDE.md` 获取详细步骤

---

## 📚 文档资源

- **使用指南**: `USAGE_GUIDE.md`
- **API 密钥**: `API_KEYS_GUIDE.md`
- **快速配置**: `QUICK_CONFIG.md`
- **系统状态**: `SYSTEM_STATUS.md`
- **完整文档**: `README.md`

---

## ✅ 系统状态

- ✅ 服务运行中
- ✅ 数据库已配置
- ✅ 所有依赖已安装
- ⚠️ API 密钥待配置（可选）

---

## 🎯 下一步

1. **访问 API 文档**: http://localhost:8000/docs
2. **测试功能**: 在 API 文档中测试端点
3. **配置密钥**: 准备好后运行 `python configure_api_keys.py`
4. **开始使用**: 系统已就绪！

---

**提示**: 在浏览器中打开 http://localhost:8000/docs 开始探索系统功能！

