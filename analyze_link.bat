@echo off
chcp 65001 >nul
echo ========================================
echo   闲鱼商品链接快速分析工具
echo ========================================
echo.

if "%~1"=="" (
    echo 用法: analyze_link.bat ^<商品链接^> [分析标准文件]
    echo.
    echo 示例:
    echo   analyze_link.bat https://www.goofish.com/item/i123456
    echo   analyze_link.bat https://www.goofish.com/item/i123456 prompts/macbook_criteria.txt
    echo.
    pause
    exit /b 1
)

python analyze_single.py %*

if %errorlevel% neq 0 (
    echo.
    echo ❌ 分析失败，请检查错误信息
    pause
    exit /b 1
)

pause
