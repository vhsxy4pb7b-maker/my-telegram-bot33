# 完整工作流程监控脚本
# 监控从webhook接收到AI回复发送的完整流程

param(
    [int]$Tail = 50  # 默认显示最新50行
)

$logFile = "logs\app.log"

if (-not (Test-Path $logFile)) {
    Write-Host "日志文件不存在: $logFile" -ForegroundColor Red
    exit 1
}

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "完整工作流程监控" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "监控流程:" -ForegroundColor Yellow
Write-Host "  1. Webhook接收消息" -ForegroundColor Gray
Write-Host "  2. 消息过滤处理" -ForegroundColor Gray
Write-Host "  3. AI回复生成" -ForegroundColor Green
Write-Host "  4. 发送AI回复" -ForegroundColor Cyan
Write-Host "  5. 错误信息" -ForegroundColor Red
Write-Host ""
Write-Host "按 Ctrl+C 停止监控" -ForegroundColor Gray
Write-Host ""

# 监控日志文件变化
Get-Content $logFile -Tail $Tail -Wait | Select-String -Pattern "webhook|Received.*message|filter|Generated reply|Sending AI reply|使用页面.*Token|未找到页面|HTTP.*200|HTTP.*500|ERROR|Exception" | ForEach-Object {
    $line = $_.Line
    $timestamp = ($line -split '\|')[0]
    
    # 高亮显示不同类型的信息
    if ($line -match "webhook|Received.*message") {
        Write-Host "[WEBHOOK] $line" -ForegroundColor Magenta
    }
    elseif ($line -match "filter|垃圾信息|无效沟通") {
        Write-Host "[FILTER] $line" -ForegroundColor Yellow
    }
    elseif ($line -match "Generated reply") {
        Write-Host "[AI生成] $line" -ForegroundColor Green
    }
    elseif ($line -match "Sending AI reply") {
        Write-Host "[发送] $line" -ForegroundColor Cyan
    }
    elseif ($line -match "使用页面.*Token|未找到页面") {
        Write-Host "[TOKEN] $line" -ForegroundColor Blue
    }
    elseif ($line -match "HTTP.*200") {
        Write-Host "[成功] $line" -ForegroundColor Green
    }
    elseif ($line -match "HTTP.*500|HTTP.*400") {
        Write-Host "[错误] $line" -ForegroundColor Red
    }
    elseif ($line -match "ERROR|Exception") {
        Write-Host "[错误] $line" -ForegroundColor Red
    }
    else {
        Write-Host $line
    }
}

