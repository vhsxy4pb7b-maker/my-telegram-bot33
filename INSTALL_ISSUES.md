# 依赖安装问题诊断

## 当前状态

### ✅ 已成功安装的包
- alembic
- pydantic
- pydantic_settings
- telegram (python-telegram-bot)
- httpx

### ❌ 未成功安装的包
- fastapi
- uvicorn
- sqlalchemy
- openai
- pyyaml
- python-dotenv
- psycopg2-binary

## 可能的原因

1. **Python 环境警告**: 检测到 `WARNING: Ignoring invalid distribution ~tarlette`，可能表示环境有问题
2. **权限问题**: 可能需要管理员权限
3. **网络问题**: 虽然使用了镜像源，但可能仍有连接问题
4. **pip 缓存问题**: 可能需要清理缓存

## 解决方案

### 方案 1：清理并重新安装

```powershell
# 清理 pip 缓存
python -m pip cache purge

# 升级 pip
python -m pip install --upgrade pip

# 重新安装（使用详细输出）
python -m pip install fastapi uvicorn sqlalchemy openai pyyaml python-dotenv psycopg2-binary -i https://pypi.tuna.tsinghua.edu.cn/simple -v
```

### 方案 2：使用管理员权限

1. 以管理员身份打开 PowerShell
2. 导航到项目目录
3. 运行安装命令

### 方案 3：修复损坏的包

```powershell
# 修复 tarlette 包（如果存在）
python -m pip uninstall tarlette -y
python -m pip install starlette
```

### 方案 4：使用虚拟环境（推荐）

```powershell
# 删除现有虚拟环境
Remove-Item -Recurse -Force venv

# 重新创建
python -m venv venv

# 激活（如果 PowerShell 执行策略允许）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# 在虚拟环境中安装
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方案 5：手动验证安装

运行以下命令查看实际安装情况：

```powershell
# 查看所有已安装的包
python -m pip list

# 查看特定包的详细信息
python -m pip show fastapi
python -m pip show uvicorn
```

## 临时解决方案

如果依赖安装一直有问题，可以：

1. **先配置其他部分**：
   - 配置 `.env` 文件中的 API 密钥
   - 设置 PostgreSQL 数据库
   - 查看文档了解系统架构

2. **使用 Docker**（如果有）：
   - 使用 Docker 容器可以避免环境问题

3. **联系技术支持**：
   - 提供完整的错误信息
   - 提供 Python 和 pip 版本信息

## 检查命令

运行以下命令获取诊断信息：

```powershell
# Python 信息
python --version
python -m pip --version

# 已安装的包
python -m pip list

# pip 配置
python -m pip config list
```

## 下一步

1. 尝试方案 1（清理并重新安装）
2. 如果失败，尝试方案 4（使用虚拟环境）
3. 如果仍然失败，请检查是否有防火墙或代理阻止了 pip 安装

