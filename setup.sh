#!/bin/bash
# 你说我画 - 环境安装脚本 (Linux/Mac)

echo "========================================"
echo "  🥧 你说我画 - 环境安装"
echo "  You Say I Draw - Setup"
echo "========================================"
echo ""

# 创建 conda 环境
echo "[1/4] 创建 conda 环境 (you-say-i-draw)..."
conda create -n you-say-i-draw python=3.10 -y

# 激活环境
echo "[2/4] 激活环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate you-say-i-draw

# 安装依赖
echo "[3/4] 安装 Python 依赖包..."
pip install -r requirements.txt

# 创建 .env 文件
echo "[4/4] 配置环境变量..."
if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建"
    echo "💡 请编辑 .env 文件，填入你的 API 密钥"
else
    echo "⚠️  .env 文件已存在，跳过"
fi

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "📝 下一步："
echo "  1. 编辑 .env 文件: nano .env 或 vim .env"
echo "  2. 运行应用: ./start.sh"
echo ""
