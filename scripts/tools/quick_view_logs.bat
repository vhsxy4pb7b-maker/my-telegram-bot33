@echo off
chcp 65001 >nul
echo ======================================================================
echo 快速查看最新日志
echo ======================================================================
echo.

powershell -ExecutionPolicy Bypass -Command "Get-Content logs\app.log -Tail 50 | Select-String -Pattern 'Generated reply|Sending AI reply|垃圾信息|webhook|ERROR'"

echo.
echo ======================================================================
pause

