@echo off
chcp 65001 >nul
echo ======================================================================
echo AI自动回复监控已启动
echo ======================================================================
echo.
echo 正在监控日志文件...
echo 请向Facebook页面发送测试消息
echo 按 Ctrl+C 停止监控
echo.
echo ======================================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0monitor_full_workflow.ps1"

