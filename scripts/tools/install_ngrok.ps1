# ngrok 安装脚本
# 这个脚本会帮助您下载并安装 ngrok

Write-Host "========================================"
Write-Host "ngrok 安装助手"
Write-Host "========================================"
Write-Host ""

# 检查是否已安装
$ngrok = Get-Command ngrok -ErrorAction SilentlyContinue
if ($ngrok) {
    Write-Host "✅ ngrok 已经安装！"
    Write-Host "📍 路径: $($ngrok.Source)"
    Write-Host ""
    Write-Host "版本信息:"
    ngrok version
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 0
}

Write-Host "检测到 ngrok 未安装，开始安装..."
Write-Host ""

# 方法 1: 尝试使用 winget
$winget = Get-Command winget -ErrorAction SilentlyContinue
if ($winget) {
    Write-Host "方法 1: 使用 winget 安装..."
    Write-Host ""
    try {
        winget install ngrok.ngrok --accept-package-agreements --accept-source-agreements
        Write-Host ""
        Write-Host "✅ ngrok 安装完成！"
        
        # 刷新 PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # 验证安装
        Start-Sleep -Seconds 2
        $ngrok = Get-Command ngrok -ErrorAction SilentlyContinue
        if ($ngrok) {
            Write-Host "✅ 验证成功！ngrok 已可用"
            ngrok version
            Read-Host "`n按 Enter 键退出"
            exit 0
        }
    } catch {
        Write-Host "⚠️  winget 安装失败，尝试其他方法..."
        Write-Host ""
    }
}

# 方法 2: 手动下载
Write-Host "方法 2: 手动下载安装"
Write-Host ""
Write-Host "请按照以下步骤操作:"
Write-Host ""
Write-Host "步骤 1: 下载 ngrok"
Write-Host "  访问: https://ngrok.com/download"
Write-Host "  或直接下载: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
Write-Host ""
Write-Host "步骤 2: 解压文件"
Write-Host "  解压到任意目录，例如: C:\ngrok"
Write-Host ""
Write-Host "步骤 3: 添加到 PATH（推荐）"
Write-Host "  1. 右键 '此电脑' -> '属性' -> '高级系统设置'"
Write-Host "  2. 点击 '环境变量'"
Write-Host "  3. 在 '系统变量' 中找到 'Path'，点击 '编辑'"
Write-Host "  4. 点击 '新建'，添加 ngrok.exe 所在目录（如 C:\ngrok）"
Write-Host "  5. 点击 '确定' 保存所有对话框"
Write-Host ""
Write-Host "步骤 4: 验证安装"
Write-Host "  关闭并重新打开 PowerShell，然后运行: ngrok version"
Write-Host ""
Write-Host "或者，不添加到 PATH，直接使用完整路径运行 ngrok"
Write-Host "  例如: C:\ngrok\ngrok.exe http 8000"
Write-Host ""

# 询问是否要打开下载页面
$openBrowser = Read-Host "是否要打开 ngrok 下载页面？(Y/N)"
if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
    Start-Process "https://ngrok.com/download"
    Write-Host ""
    Write-Host "✅ 已打开下载页面"
}

Write-Host ""
Read-Host "按 Enter 键退出"

