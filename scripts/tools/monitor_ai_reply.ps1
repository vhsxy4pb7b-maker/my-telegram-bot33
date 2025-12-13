# AI自动回复实时监控脚本
# 监控AI回复生成和发送过程

param(
    [int]$Tail = 100  # 默认显示最新100行
)

$logFile = "logs\app.log"

if (-not (Test-Path $logFile)) {
    Write-Host "日志文件不存在: $logFile" -ForegroundColor Red
    exit 1
}

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "AI自动回复实时监控" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "监控关键词:" -ForegroundColor Yellow
Write-Host "  - Generated reply (AI回复生成)" -ForegroundColor Green
Write-Host "  - Sending AI reply (发送AI回复)" -ForegroundColor Green
Write-Host "  - 垃圾信息/无效沟通 (过滤消息)" -ForegroundColor Yellow
Write-Host "  - 跳过回复 (跳过处理)" -ForegroundColor Yellow
Write-Host "  - ERROR (错误信息)" -ForegroundColor Red
Write-Host ""
Write-Host "按 Ctrl+C 停止监控" -ForegroundColor Gray
Write-Host ""

# 监控日志文件变化
Get-Content $logFile -Tail $Tail -Wait | Select-String -Pattern "Generated reply|Sending AI reply|垃圾信息|无效沟通|跳过回复|AI回复|ERROR.*reply|reply.*ERROR" | ForEach-Object {
    $line = $_.Line
    
    # 高亮显示不同类型的信息
    if ($line -match "Generated reply") {
        Write-Host $line -ForegroundColor Green
    }
    elseif ($line -match "Sending AI reply") {
        Write-Host $line -ForegroundColor Cyan
    }
    elseif ($line -match "垃圾信息|无效沟通|跳过回复") {
        Write-Host $line -ForegroundColor Yellow
    }
    elseif ($line -match "ERROR") {
        Write-Host $line -ForegroundColor Red
    }
    else {
        Write-Host $line
    }
}

