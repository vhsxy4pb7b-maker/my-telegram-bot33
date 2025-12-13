@echo off
REM ngrok 安装脚本（批处理版本）

echo ========================================
echo ngrok 安装助手
echo ========================================
echo.

REM 检查是否已安装
where ngrok >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ ngrok 已经安装！
    echo.
    ngrok version
    echo.
    pause
    exit /b 0
)

echo 检测到 ngrok 未安装，开始安装...
echo.

REM 尝试使用 winget
where winget >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo 方法 1: 使用 winget 安装...
    echo.
    winget install ngrok.ngrok --accept-package-agreements --accept-source-agreements
    echo.
    
    REM 验证安装
    timeout /t 2 /nobreak >nul
    where ngrok >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ ngrok 安装完成！
        echo.
        ngrok version
        echo.
        pause
        exit /b 0
    )
)

REM 手动安装说明
echo 方法 2: 手动下载安装
echo.
echo 请按照以下步骤操作:
echo.
echo 步骤 1: 下载 ngrok
echo   访问: https://ngrok.com/download
echo   或直接下载: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip
echo.
echo 步骤 2: 解压文件
echo   解压到任意目录，例如: C:\ngrok
echo.
echo 步骤 3: 添加到 PATH（推荐）
echo   1. 右键 '此电脑' -^> '属性' -^> '高级系统设置'
echo   2. 点击 '环境变量'
echo   3. 在 '系统变量' 中找到 'Path'，点击 '编辑'
echo   4. 点击 '新建'，添加 ngrok.exe 所在目录（如 C:\ngrok）
echo   5. 点击 '确定' 保存所有对话框
echo.
echo 步骤 4: 验证安装
echo   关闭并重新打开 PowerShell，然后运行: ngrok version
echo.
echo 或者，不添加到 PATH，直接使用完整路径运行 ngrok
echo   例如: C:\ngrok\ngrok.exe http 8000
echo.

REM 询问是否要打开下载页面
set /p OPEN_BROWSER="是否要打开 ngrok 下载页面？(Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    start https://ngrok.com/download
    echo.
    echo ✅ 已打开下载页面
)

echo.
pause

