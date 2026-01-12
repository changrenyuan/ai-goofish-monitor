@echo off
chcp 65001 >nul
title 闲鱼智能监控机器人 - 安装脚本

echo ========================================
echo    闲鱼智能监控机器人
echo    Windows 一键安装脚本
echo ========================================
echo.

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo 此脚本将自动安装所有依赖，预计需要 10-15 分钟。
echo.
pause

echo.
echo [1/7] 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python！请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

echo.
echo [2/7] 检查 Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js！请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)
node --version
npm --version

echo.
echo [3/7] 创建虚拟环境...
if not exist ".venv" (
    python -m venv .venv
    echo 虚拟环境创建成功
) else (
    echo 虚拟环境已存在，跳过创建
)

echo.
echo [4/7] 激活虚拟环境...
call .venv\Scripts\activate.bat

echo.
echo [5/7] 安装 Python 依赖...
echo 这可能需要几分钟...
pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo [错误] Python 依赖安装失败！
    pause
    exit /b 1
)

echo.
echo [6/7] 安装 Playwright 浏览器...
echo 这可能需要几分钟...
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium

if errorlevel 1 (
    echo [警告] Playwright 安装失败，请手动运行: playwright install chromium
)

echo.
echo [7/7] 构建前端...
cd web-ui
echo 正在安装前端依赖...
npm install --registry=https://registry.npmmirror.com

if errorlevel 1 (
    echo [错误] 前端依赖安装失败！
    pause
    exit /b 1
)

echo 正在构建前端...
npm run build

if errorlevel 1 (
    echo [错误] 前端构建失败！
    pause
    exit /b 1
)

cd ..

echo.
echo [8/7] 创建配置文件...
if not exist ".env" (
    copy .env.example .env >nul
    echo 已创建 .env 文件
) else (
    echo .env 文件已存在
)

if not exist "config.json" (
    copy config.json.example config.json >nul
    echo 已创建 config.json 文件
) else (
    echo config.json 文件已存在
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 接下来的步骤：
echo 1. 打开 .env 文件，配置以下内容：
echo    - OPENAI_API_KEY（必填）
echo    - OPENAI_BASE_URL（必填）
echo    - OPENAI_MODEL_NAME（必填）
echo.
echo 2. 运行服务：
echo    双击 start.bat
echo    或在 PyCharm 中运行 src/app.py
echo.
echo 3. 访问 Web 界面：
echo    http://localhost:5000
echo    默认账号: admin / admin123
echo.
echo 详细文档: WINDOWS_DEPLOYMENT.md
echo.
pause
