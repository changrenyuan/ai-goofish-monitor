@echo off
chcp 65001 >nul
title Gemini API 配置助手

echo ========================================
echo   Gemini API 配置助手
echo ========================================
echo.

REM 检查 .env 文件是否存在
if not exist ".env" (
    echo [错误] 未找到 .env 文件！
    echo 正在从 .env.example 创建...
    copy .env.example .env >nul
    echo 已创建 .env 文件
    echo.
)

echo 请按照提示输入 Gemini API 配置信息
echo (按 Ctrl+C 取消)
echo.

REM 获取 API Key
set /p API_KEY="请输入 Gemini API Key: "

REM 选择模型
echo.
echo 可用的 Gemini 模型：
echo   1. gemini-2.0-flash-exp (最新，快速，多模态) ★推荐
echo   2. gemini-1.5-pro (稳定，多模态)
echo   3. gemini-1.5-flash (快速，多模态)
echo.

set /p MODEL_CHOICE="请选择模型 (1-3，默认 1): "

if "%MODEL_CHOICE%"=="" set MODEL_CHOICE=1
if "%MODEL_CHOICE%"=="1" set MODEL_NAME=gemini-2.0-flash-exp
if "%MODEL_CHOICE%"=="2" set MODEL_NAME=gemini-1.5-pro
if "%MODEL_CHOICE%"=="3" set MODEL_NAME=gemini-1.5-flash

echo.
echo 你选择的模型: %MODEL_NAME%
echo.

REM 确认配置
echo 配置摘要：
echo   API Key: %API_KEY:~0,20%...
echo   Base URL: https://generativelanguage.googleapis.com/v1beta/openai/
echo   Model: %MODEL_NAME%
echo.
set /p CONFIRM="确认配置？(Y/n): "

if /i not "%CONFIRM%"=="n" if /i not "%CONFIRM%"=="no" (
    echo.
    echo 正在更新 .env 文件...

    REM 使用 PowerShell 读取并更新 .env 文件
    powershell -Command "(Get-Content .env) -replace '^OPENAI_API_KEY=.*', ('OPENAI_API_KEY=\"' + '%API_KEY%' + '\"') | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace '^OPENAI_BASE_URL=.*', 'OPENAI_BASE_URL=\"https://generativelanguage.googleapis.com/v1beta/openai/\"' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace '^OPENAI_MODEL_NAME=.*', ('OPENAI_MODEL_NAME=\"%MODEL_NAME%\"') | Set-Content .env"

    echo.
    echo ✅ 配置完成！
    echo.
    echo 下一步：
    echo   1. 运行 start.bat 启动服务
    echo   2. 访问 http://localhost:5000
    echo   3. 登录: admin / admin123
    echo.
    echo 📖 更多信息: GEMINI_API_CONFIG.md
) else (
    echo.
    echo 已取消配置。
)

pause
