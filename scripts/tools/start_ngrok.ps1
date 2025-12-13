# 启动 ngrok 脚本（PowerShell 版本）
# 这个脚本会在新窗口中启动 ngrok

Write-Host "========================================"
Write-Host "启动 ngrok"
Write-Host "========================================"
Write-Host ""

# 获取当前目录（脚本所在目录的上级目录的上级目录）
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

# 检查 ngrok 是否在 PATH 中
$ngrok = Get-Command ngrok -ErrorAction SilentlyContinue

if (-not $ngrok) {
    Write-Host "❌ 错误: 未找到 ngrok"
    Write-Host ""
    Write-Host "请先安装 ngrok:"
    Write-Host "  1. 访问 https://ngrok.com/download"
    Write-Host "  2. 下载 Windows 版本"
    Write-Host "  3. 解压到任意目录"
    Write-Host "  4. 将 ngrok.exe 添加到 PATH 或使用完整路径"
    Write-Host ""
    Write-Host "或者，如果您知道 ngrok.exe 的完整路径，"
    Write-Host "可以修改此脚本中的路径。"
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host "✅ 找到 ngrok: $($ngrok.Source)"
Write-Host ""
Write-Host "正在新窗口中启动 ngrok http 8000..."
Write-Host ""

# 在新窗口中启动 ngrok
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; ngrok http 8000; Write-Host '`n按任意键关闭...'; Read-Host"

Write-Host "✅ ngrok 已在新窗口中启动"
Write-Host ""
Write-Host "📋 下一步:"
Write-Host "  1. 在新窗口中查看 ngrok 输出"
Write-Host "  2. 复制 ngrok 提供的 HTTPS 地址（类似: https://xxxx.ngrok-free.app）"
Write-Host "  3. 在 Facebook 开发者控制台配置 Webhook URL"
Write-Host ""
Read-Host "按 Enter 键退出"

