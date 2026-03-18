@echo off
chcp 65001 >nul
title 停止币安行情Dashboard

echo ================================================
echo        停止币安行情Dashboard
echo ================================================
echo.

echo 正在停止所有服务...

:: 停止所有node进程 (前端)
echo   - 停止前端服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "3000 3001 3002" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: 查找并停止Python后端
echo   - 停止后端服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: 停止残留的node进程
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1

echo.
echo ✓ 所有服务已停止
echo ================================================

timeout /t 2 /nobreak >nul