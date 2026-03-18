@echo off
chcp 65001 >nul
title 币安行情Dashboard

echo ================================================
echo        币安行情Dashboard 启动器
echo ================================================
echo.

cd /d "%~dp0"

echo [1/2] 检查并安装依赖...
if not exist "binance-dashboard\node_modules" (
    echo   安装前端依赖中...
    cd binance-dashboard
    call npm install
    cd ..
    echo   ✓ 依赖安装完成
) else (
    echo   ✓ 依赖已安装
)

echo.
echo [2/2] 启动服务...
echo.

start "Binance Backend" cmd /k "python binance_server.py"
timeout /t 2 /nobreak >nul

start "Binance Frontend" cmd /k "cd binance-dashboard && npm run dev"
timeout /t 3 /nobreak >nul

echo ================================================
echo   启动完成!
echo.
echo   后端地址: http://localhost:5000
echo   前端地址: http://localhost:3000
echo   (前端如端口被占用会自动切换)
echo.
echo   停止服务请运行: python run.py stop
echo ================================================

echo.
pause