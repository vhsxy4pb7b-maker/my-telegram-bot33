# 虚拟环境激活脚本
# 使用方法：在 PowerShell 中运行 .\activate_venv.ps1

$venvPython = ".\venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    Write-Host "使用虚拟环境中的 Python..." -ForegroundColor Green
    & $venvPython -m pip install -r requirements.txt
} else {
    Write-Host "虚拟环境未找到，使用系统 Python..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

Write-Host "`n安装完成！" -ForegroundColor Green
Write-Host "要使用虚拟环境，请运行: .\venv\Scripts\python.exe your_script.py" -ForegroundColor Cyan


