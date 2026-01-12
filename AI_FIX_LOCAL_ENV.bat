@echo off
echo ====================================================
echo  本地 AI 配置修复工具
echo ====================================================
echo.

if not exist ".env" (
    echo [ERROR] .env 文件不存在
    pause
    exit /b 1
)

echo [INFO] 正在更新 .env 文件中的 AI 配置...
echo.

REM 备份原文件
copy .env .env.backup >nul 2>&1
echo [INFO] 已备份原 .env 文件为 .env.backup

REM 使用 PowerShell 替换配置
powershell -Command "(Get-Content .env) -replace '^OPENAI_API_KEY=.*', 'OPENAI_API_KEY=\"sk-74d54050a12e490caf2abcbe246db64b\"' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^OPENAI_BASE_URL=.*', 'OPENAI_BASE_URL=\"https://dashscope.aliyuncs.com/compatible-mode/v1\"' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^OPENAI_MODEL_NAME=.*', 'OPENAI_MODEL_NAME=\"qwen-plus\"' | Set-Content .env"

echo.
echo [SUCCESS] .env 文件已更新！
echo.
echo 配置信息:
echo   API Key: sk-74d54050a12e490caf2abcbe246db64b
echo   Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
echo   Model: qwen-plus
echo.
echo ====================================================
echo  请重启应用使配置生效
echo ====================================================
pause
