@echo off
cd /d %~dp0
echo 正在推送代码到 GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo 推送成功！请刷新 https://daily.zhimai-ai.cn 查看更新
) else (
    echo.
    echo 推送失败，请检查网络连接
)
pause
