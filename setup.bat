@echo off
REM 你说我画 - 环境安装脚本

echo ========================================
echo   🥧 你说我画 - 环境安装
echo   You Say I Draw - Setup
echo ========================================
echo.

REM 创建 conda 环境
echo [1/4] 创建 conda 环境 (you-say-i-draw)...
call conda create -n you-say-i-draw python=3.10 -y
if errorlevel 1 (
    echo ❌ 环境创建失败！
    pause
    exit /b 1
)

REM 激活环境
echo [2/4] 激活环境...
call conda activate you-say-i-draw
if errorlevel 1 (
    echo ❌ 环境激活失败！
    pause
    exit /b 1
)

REM 安装依赖
echo [3/4] 安装 Python 依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败！
    pause
    exit /b 1
)

REM 创建 .env 文件
echo [4/4] 配置环境变量...
if not exist .env (
    echo 创建 .env 文件...
    copy .env.example .env
    echo ✅ .env 文件已创建
    echo 💡 请编辑 .env 文件，填入你的 API 密钥
) else (
    echo ⚠️  .env 文件已存在，跳过
)

echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 📝 下一步：
echo   1. 编辑 .env 文件，填入 API 密钥
echo   2. 双击 start.bat 启动应用
echo.
pause
