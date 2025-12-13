# ngrok 启动脚本（带检查）
# 这个脚本会检查环境并启动 ngrok

Write-Host "========================================"
Write-Host "ngrok 启动检查"
Write-Host "========================================"
Write-Host ""

# 检查应用是否运行
Write-Host "1. 检查应用是否在运行..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ 应用正在运行在 http://localhost:8000"
    Write-Host ""
} catch {
    Write-Host "   ❌ 应用未运行在 http://localhost:8000"
    Write-Host "   💡 请先启动应用: python run.py"
    Write-Host ""
    $startApp = Read-Host "是否现在启动应用？(Y/N)"
    if ($startApp -eq "Y" -or $startApp -eq "y") {
        Write-Host "   正在启动应用..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python run.py"
        Write-Host "   请等待应用启动（约 5-10 秒），然后按 Enter 继续..."
        Read-Host
    } else {
        Write-Host "   请先启动应用，然后重新运行此脚本"
        Read-Host "按 Enter 键退出"
        exit 1
    }
}

# 检查 ngrok 是否安装
Write-Host "2. 检查 ngrok 是否安装..."
$ngrok = Get-Command ngrok -ErrorAction SilentlyContinue
if (-not $ngrok) {
    Write-Host "   ❌ ngrok 未安装或不在 PATH 中"
    Write-Host "   💡 请先安装 ngrok:"
    Write-Host "      winget install ngrok.ngrok"
    Write-Host "      或访问: https://ngrok.com/download"
    Read-Host "按 Enter 键退出"
    exit 1
}
Write-Host "   ✅ ngrok 已安装: $($ngrok.Source)"
Write-Host ""

# 检查 ngrok 配置
Write-Host "3. 检查 ngrok 配置..."
try {
    $configCheck = ngrok config check 2>&1 | Out-String
    if ($configCheck -match "ERROR" -or $configCheck -match "authtoken" -or $configCheck -match "cannot find") {
        Write-Host "   ⚠️  ngrok 需要配置 authtoken"
        Write-Host ""
        Write-Host "   请按照以下步骤配置:"
        Write-Host "   1. 访问: https://dashboard.ngrok.com/signup 注册账户"
        Write-Host "   2. 获取 authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
        Write-Host "   3. 运行: ngrok config add-authtoken YOUR_TOKEN"
        Write-Host ""
        $configure = Read-Host "是否现在配置 authtoken？(Y/N)"
        if ($configure -eq "Y" -or $configure -eq "y") {
            $authtoken = Read-Host "请输入您的 authtoken"
            if ($authtoken) {
                Write-Host "   正在配置 authtoken..."
                ngrok config add-authtoken $authtoken
                Write-Host "   ✅ authtoken 已配置"
                Write-Host ""
            }
        } else {
            Write-Host "   请先配置 authtoken，然后重新运行此脚本"
            Read-Host "按 Enter 键退出"
            exit 1
        }
    } else {
        Write-Host "   ✅ ngrok 配置正常"
        Write-Host ""
    }
} catch {
    Write-Host "   ⚠️  无法检查配置，尝试继续启动..."
    Write-Host ""
}

# 启动 ngrok
Write-Host "4. 启动 ngrok..."
Write-Host ""
Write-Host "========================================"
Write-Host "ngrok 正在启动..."
Write-Host "========================================"
Write-Host ""
Write-Host "如果看到 'Forwarding' 行，说明启动成功"
Write-Host "例如: https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8000"
Write-Host ""
Write-Host "按 Ctrl+C 停止 ngrok"
Write-Host ""

ngrok http 8000

