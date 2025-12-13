@echo off
REM 启动 ngrok 脚本（批处理版本）
REM 这个脚本会在新窗口中启动 ngrok

echo ========================================
echo 启动 ngrok
echo ========================================
echo.

REM 检查 ngrok 是否在 PATH 中
where ngrok >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 ngrok
    echo.
    echo 请先安装 ngrok:
    echo   1. 访问 https://ngrok.com/download
    echo   2. 下载 Windows 版本
    echo   3. 解压到任意目录
    echo   4. 将 ngrok.exe 添加到 PATH 或使用完整路径
    echo.
    echo 或者，如果您知道 ngrok.exe 的完整路径，
    echo 可以修改此脚本中的路径。
    pause
    exit /b 1
)

echo ✅ 找到 ngrok
echo.
echo 正在新窗口中启动 ngrok http 8000...
echo.

REM 获取当前目录
set CURRENT_DIR=%~dp0..\..

REM 在新窗口中启动 ngrok
start "ngrok" cmd /k "cd /d "%CURRENT_DIR%" && ngrok http 8000"

echo ✅ ngrok 已在新窗口中启动
echo.
echo 📋 下一步:
echo   1. 在新窗口中查看 ngrok 输出
echo   2. 复制 ngrok 提供的 HTTPS 地址（类似: https://xxxx.ngrok-free.app）
echo   3. 在 Facebook 开发者控制台配置 Webhook URL
echo.
pause
