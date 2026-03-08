#!/bin/bash
# 你说我画 - 启动脚本 (Linux/Mac)

echo "========================================"
echo "  🥧 你说我画 - You Say I Draw"
echo "  Pi Day 数学绘图游戏"
echo "========================================"
echo ""

# 激活 conda 环境
echo "[1/3] 激活 conda 环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate you-say-i-draw

# 检查 .env 文件
echo "[2/3] 检查配置..."
if [ ! -f .env ]; then
    echo "⚠️  警告: .env 文件不存在"
    echo "💡 请复制 .env.example 为 .env 并配置 API 密钥"
    echo ""
    read -p "按 Enter 继续..."
fi

# 启动 Streamlit
echo "[3/3] 启动应用..."
echo ""
streamlit run app.py
