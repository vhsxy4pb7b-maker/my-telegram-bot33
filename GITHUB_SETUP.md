# GitHub 仓库设置指南

## ✅ Git 初始化完成

项目已初始化为 Git 仓库，代码已提交。

## 📋 下一步：创建 GitHub 仓库

### 步骤 1: 在 GitHub 创建新仓库

1. **访问**: https://github.com/new
2. **填写信息**:
   - **Repository name**: 输入仓库名称（如：`customer-service`）
   - **Description**: 可选，描述项目
   - **Visibility**: 选择 Public 或 Private
   - ⚠️ **重要**: **不要**勾选以下选项：
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
3. **点击**: "Create repository"

### 步骤 2: 复制仓库 URL

创建后，GitHub 会显示仓库 URL，类似：
```
https://github.com/你的用户名/仓库名.git
```

### 步骤 3: 连接并推送代码

在本地项目目录执行以下命令（替换为你的实际仓库 URL）：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 设置主分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

## 🔐 认证方式

### 方式 1: 使用 Personal Access Token（推荐）

如果提示需要认证：

1. **生成 Token**:
   - 访问: https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 生成并复制 Token

2. **推送时使用 Token**:
   ```bash
   git push -u origin main
   # 用户名: 你的GitHub用户名
   # 密码: 使用刚才生成的Token
   ```

### 方式 2: 使用 SSH（推荐用于长期使用）

1. **生成 SSH 密钥**（如果还没有）:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **添加 SSH 密钥到 GitHub**:
   - 复制公钥: `cat ~/.ssh/id_ed25519.pub`
   - 访问: https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥并保存

3. **使用 SSH URL**:
   ```bash
   git remote set-url origin git@github.com:你的用户名/仓库名.git
   git push -u origin main
   ```

## ✅ 验证推送

推送成功后，访问你的 GitHub 仓库页面，应该能看到所有文件。

## 🚀 下一步：部署到 Railway

代码推送到 GitHub 后：

1. 访问 https://railway.app
2. 登录（使用 GitHub 账号）
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的仓库
6. Railway 会自动开始部署

详细步骤请参考：[DEPLOY_STEPS.md](DEPLOY_STEPS.md)

## 📝 常用 Git 命令

```bash
# 查看状态
git status

# 查看远程仓库
git remote -v

# 查看提交历史
git log --oneline

# 添加新文件
git add .
git commit -m "提交信息"

# 推送到 GitHub
git push

# 拉取最新代码
git pull
```

