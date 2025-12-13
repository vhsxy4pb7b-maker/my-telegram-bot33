# 实时监控日志，用于测试消息处理
# 使用方法: .\scripts\tools\monitor_test_message.ps1

Write-Host "`n=== 实时日志监控（用于测试消息） ===" -ForegroundColor Green
Write-Host "监控关键词: 使用页面|未找到页面|Sending AI reply|Generated reply|ERROR|webhook`n" -ForegroundColor Cyan

$logFile = "logs\app.log"
$keywords = "使用页面|未找到页面|Sending AI reply|Generated reply|ERROR|webhook|messaging"

if (-not (Test-Path $logFile)) {
    Write-Host "❌ 日志文件不存在: $logFile" -ForegroundColor Red
    exit 1
}

Write-Host "📝 开始监控日志..." -ForegroundColor Yellow
Write-Host "💡 提示: 请向Facebook页面发送一条测试消息" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止监控`n" -ForegroundColor Gray

# 获取文件初始大小
$lastSize = (Get-Item $logFile).Length

try {
    while ($true) {
        $currentSize = (Get-Item $logFile).Length
        
        if ($currentSize -gt $lastSize) {
            # 读取新增的内容
            $stream = [System.IO.File]::OpenRead($logFile)
            $stream.Position = $lastSize
            $reader = New-Object System.IO.StreamReader($stream)
            
            while ($null -ne ($line = $reader.ReadLine())) {
                if ($line -match $keywords) {
                    $timestamp = Get-Date -Format "HH:mm:ss"
                    Write-Host "[$timestamp] $line" -ForegroundColor White
                }
            }
            
            $reader.Close()
            $stream.Close()
            $lastSize = $currentSize
        }
        
        Start-Sleep -Milliseconds 500
    }
} catch {
    Write-Host "`n监控已停止" -ForegroundColor Yellow
}

