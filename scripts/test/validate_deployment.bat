@echo off
REM 部署验证脚本 (Windows)

echo ==========================================
echo 部署验证 - 系统1.0版本
echo ==========================================
echo.

set PASS_COUNT=0
set FAIL_COUNT=0

REM 1. 检查配置文件
echo 1. 配置文件检查
echo ----------------------------------------
if exist .env (
    echo [PASS] .env文件存在
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] .env文件不存在
    set /a FAIL_COUNT+=1
)

if exist config\config.yaml (
    echo [PASS] config.yaml存在
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] config.yaml不存在
    set /a FAIL_COUNT+=1
)

REM 2. 检查数据库连接
echo.
echo 2. 数据库连接检查
echo ----------------------------------------
python -c "from src.database.database import engine; engine.connect()" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] 数据库连接正常
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] 数据库连接失败
    set /a FAIL_COUNT+=1
)

REM 3. 检查应用启动
echo.
echo 3. 应用启动检查
echo ----------------------------------------
python -c "from src.main import app; assert app is not None" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] FastAPI应用创建成功
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] FastAPI应用创建失败
    set /a FAIL_COUNT+=1
)

REM 4. 检查日志目录
echo.
echo 4. 日志目录检查
echo ----------------------------------------
if exist logs (
    echo [PASS] logs目录存在
    set /a PASS_COUNT+=1
) else (
    mkdir logs
    echo [PASS] logs目录已创建
    set /a PASS_COUNT+=1
)

REM 总结
echo.
echo ==========================================
echo 验证总结
echo ==========================================
echo 通过: %PASS_COUNT%
echo 失败: %FAIL_COUNT%
echo.

if %FAIL_COUNT% equ 0 (
    echo [SUCCESS] 部署验证通过！系统可以部署。
    exit /b 0
) else (
    echo [ERROR] 发现 %FAIL_COUNT% 个问题，请修复后再部署。
    exit /b 1
)

