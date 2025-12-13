@echo off
REM 快速测试脚本 - 验证系统1.0版本基本功能 (Windows)

echo ==========================================
echo 系统1.0版本快速测试
echo ==========================================
echo.

set PASS_COUNT=0
set FAIL_COUNT=0
set SKIP_COUNT=0

REM 1. 检查Python版本
echo 1. 环境检查
echo ----------------------------------------
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Python已安装
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] Python未安装
    set /a FAIL_COUNT+=1
)

REM 2. 检查依赖
echo.
echo 2. 依赖检查
echo ----------------------------------------
if exist requirements.txt (
    echo [PASS] requirements.txt存在
    set /a PASS_COUNT+=1
    
    python -c "import fastapi" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [PASS] 依赖已安装
        set /a PASS_COUNT+=1
    ) else (
        echo [FAIL] 依赖未安装
        set /a FAIL_COUNT+=1
    )
) else (
    echo [FAIL] requirements.txt不存在
    set /a FAIL_COUNT+=1
)

REM 3. 检查配置文件
echo.
echo 3. 配置文件检查
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
) else if exist config\config.yaml.example (
    echo [SKIP] config.yaml不存在，但example存在
    set /a SKIP_COUNT+=1
) else (
    echo [FAIL] config.yaml和example都不存在
    set /a FAIL_COUNT+=1
)

REM 4. 测试配置加载
echo.
echo 4. 配置加载测试
echo ----------------------------------------
python -c "from src.config import settings; assert hasattr(settings, 'database_url')" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] 环境变量配置加载
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] 环境变量配置加载失败
    set /a FAIL_COUNT+=1
)

REM 5. 测试数据库模型
echo.
echo 5. 数据库模型测试
echo ----------------------------------------
python -c "from src.database.models import Customer, Conversation" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] 数据库模型导入
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] 数据库模型导入失败
    set /a FAIL_COUNT+=1
)

REM 6. 测试核心模块
echo.
echo 6. 核心模块测试
echo ----------------------------------------
python -c "from src.facebook.api_client import FacebookAPIClient" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Facebook模块导入
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] Facebook模块导入失败
    set /a FAIL_COUNT+=1
)

python -c "from src.ai.reply_generator import ReplyGenerator" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] AI模块导入
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] AI模块导入失败
    set /a FAIL_COUNT+=1
)

REM 7. 测试应用启动
echo.
echo 7. 应用启动测试
echo ----------------------------------------
python -c "from src.main import app; assert app is not None" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] FastAPI应用创建
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] FastAPI应用创建失败
    set /a FAIL_COUNT+=1
)

REM 总结
echo.
echo ==========================================
echo 测试总结
echo ==========================================
echo 通过: %PASS_COUNT%
echo 失败: %FAIL_COUNT%
echo 跳过: %SKIP_COUNT%
echo.

if %FAIL_COUNT% equ 0 (
    echo [SUCCESS] 所有关键测试通过！系统基本功能正常。
    exit /b 0
) else (
    echo [ERROR] 发现 %FAIL_COUNT% 个失败项，请检查并修复。
    exit /b 1
)

