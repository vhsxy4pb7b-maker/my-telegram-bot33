# Log viewer tool
# Usage: .\scripts\tools\view_logs.ps1 [type] [lines]

param(
    [Parameter(Position=0)]
    [ValidateSet("token", "messages", "errors", "all", "latest")]
    [string]$Type = "all",
    
    [int]$Lines = 50
)

$logFile = "logs\app.log"

if (-not (Test-Path $logFile)) {
    Write-Host "Log file not found: $logFile" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Log Viewer Tool" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Log file: $logFile" -ForegroundColor Cyan
Write-Host "View type: $Type" -ForegroundColor Cyan
Write-Host "Lines: $Lines" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

switch ($Type) {
    "token" {
        Write-Host "Viewing Token usage..." -ForegroundColor Yellow
        Get-Content $logFile -Tail $Lines | Select-String -Pattern "使用页面|未找到页面"
    }
    "messages" {
        Write-Host "Viewing message processing..." -ForegroundColor Yellow
        Get-Content $logFile -Tail $Lines | Select-String -Pattern "webhook|Generated reply|Sending AI reply"
    }
    "errors" {
        Write-Host "Viewing errors..." -ForegroundColor Yellow
        Get-Content $logFile -Tail $Lines | Select-String -Pattern "ERROR|Exception|500|400"
    }
    "all" {
        Write-Host "Viewing complete processing flow..." -ForegroundColor Yellow
        Get-Content $logFile -Tail $Lines | Select-String -Pattern "使用页面|未找到页面|webhook|Generated reply|Sending AI reply|ERROR|200|500"
    }
    "latest" {
        Write-Host "Viewing latest logs..." -ForegroundColor Yellow
        Get-Content $logFile -Tail $Lines
    }
}

Write-Host ""
Write-Host "View completed" -ForegroundColor Green
