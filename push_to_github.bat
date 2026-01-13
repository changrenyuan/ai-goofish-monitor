@echo off
chcp 65001 >nul
echo ========================================
echo   推送代码到 GitHub
echo ========================================
echo.
echo 正在推送到远程仓库...
echo.

git push --set-upstream origin master

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   推送失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 需要配置 GitHub 身份验证
    echo.
    echo 解决方法：
    echo.
    echo 方法1: 使用 SSH (推荐)
    echo   git remote set-url origin git@github.com:changrenyuan/ai-goofish-monitor.git
    echo   git push --set-upstream origin master
    echo.
    echo 方法2: 使用 Personal Access Token
    echo   git push https://YOUR_TOKEN@github.com/changrenyuan/ai-goofish-monitor.git master
    echo.
    echo 方法3: 配置 Git Credential Manager
    echo   git config --global credential.helper manager-core
    echo   git push --set-upstream origin master
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 推送成功！
echo ========================================
echo.
pause
