@echo off
chcp 65001 >nul
title 闲鱼智能监控机器人 - 启动脚本

echo ========================================
echo    闲鱼智能监控机器人
echo    Windows 快速启动脚本
echo ========================================
echo.

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境！
    echo.
    echo 请先执行以下步骤：
    echo 1. 打开 PyCharm
    echo 2. 配置 Python 解释器（Settings → Python Interpreter）
    echo 3. 在 Terminal 中运行: pip install -r requirements.txt
    echo 4. 在 Terminal 中运行: playwright install chromium
    echo 5. 在 Terminal 中运行: cd web-ui ^&^& npm install ^&^& npm run build
    echo.
    pause
    exit /b 1
)

REM 激活虚拟环境
echo [1/4] 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 检查 dist 目录
if not exist "dist\index.html" (
    echo [警告] 未找到前端构建产物！
    echo 请先运行: cd web-ui ^&^& npm install ^&^& npm run build
    echo.
)

REM 检查 .env 文件
if not exist ".env" (
    echo [警告] 未找到 .env 配置文件！
    echo 请先复制 .env.example 并配置 API Key
    echo.
)

echo [2/4] 检查配置完成
echo [3/4] 启动服务...
echo.
echo ========================================
echo   服务地址: http://localhost:5000
echo   默认账号: admin / admin123
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

REM 启动服务
python -m uvicorn src.app:app --host 0.0.0.0 --port 5000

pause
