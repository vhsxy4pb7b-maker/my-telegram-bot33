# Refresh and view latest logs
# Usage: .\scripts\tools\refresh_logs.ps1

param(
    [int]$Tail = 30
)

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Refresh Latest Logs" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Showing latest $Tail matching log entries..." -ForegroundColor Yellow
Write-Host ""

$pattern = "Generated reply|Sending AI reply|垃圾信息|无效沟通|webhook|ERROR|Exception"

Get-Content logs\app.log -Tail $Tail -Encoding UTF8 | Select-String -Pattern $pattern | ForEach-Object {
    $line = $_.Line
    
    if ($line -match "Generated reply") {
        Write-Host "[AI Generated] $line" -ForegroundColor Green
    }
    elseif ($line -match "Sending AI reply") {
        Write-Host "[Sending] $line" -ForegroundColor Cyan
    }
    elseif ($line -match "垃圾信息|无效沟通|跳过回复") {
        Write-Host "[Filtered] $line" -ForegroundColor Yellow
    }
    elseif ($line -match "webhook") {
        Write-Host "[WEBHOOK] $line" -ForegroundColor Magenta
    }
    elseif ($line -match "ERROR|Exception") {
        Write-Host "[ERROR] $line" -ForegroundColor Red
    }
    else {
        Write-Host $line
    }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tip: Run this script again to refresh and view latest logs" -ForegroundColor Yellow
Write-Host ""

