@echo off
chcp 65001 >nul
echo ========================================
echo   豆包 (Doubao) 模型快速配置
echo ========================================
echo.

python config_doubao.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 配置失败，请检查错误信息
    pause
    exit /b 1
)

pause
