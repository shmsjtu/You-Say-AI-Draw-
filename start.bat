@echo off
REM 你说我画 - 启动脚本

echo ========================================
echo   🥧 你说我画 - You Say I Draw
echo   Pi Day 数学绘图游戏
echo ========================================
echo.

REM 激活 conda 环境
echo [1/3] 激活 conda 环境...
call conda activate you-say-i-draw
if errorlevel 1 (
    echo ❌ 环境激活失败！请先运行 setup.bat 安装环境
    pause
    exit /b 1
)

REM 检查 .env 文件
echo [2/3] 检查配置...
if not exist .env (
    echo ⚠️  警告: .env 文件不存在
    echo 💡 请复制 .env.example 为 .env 并配置 API 密钥
    echo.
    pause
)

REM 启动 Streamlit
echo [3/3] 启动应用...
echo.
streamlit run app.py

pause
