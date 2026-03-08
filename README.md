# 🥧 你说我画 - You Say I Draw

一个为 Pi Day 设计的交互式数学绘图游戏。用户输入自然语言提示词，系统通过 LLM 将其转化为数学方程代码，并使用 matplotlib 渲染出精美的数学图形。

## ✨ 特性

- 🎨 自然语言转数学图形
- 🔒 安全的沙箱代码执行
- 🤖 支持多种 LLM（OpenAI GPT-4、Google Gemini、DeepSeek 等）
- 📊 实时图形渲染（支持 2D 和 **3D**！）
- 🌐 简洁的 Streamlit Web 界面
- 🎯 支持自定义 API Base URL（代理、本地模型等）

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆或下载项目
cd "You Say I Draw"

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
# 支持 OpenAI 或 Google Gemini
```

**.env 配置示例：**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
MODEL_NAME=gpt-4
TEMPERATURE=0.7
```

### 3. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

## 🎮 使用方法

1. 在输入框中输入你的想象，例如：

   **2D 图形：**
   - "画一个笑脸"
   - "画一个愤怒的包子"
   - "画一朵玫瑰花"
   - "画一个心形"

   **3D 图形：** ✨ 新功能！
   - "画一个 3D 螺旋"
   - "画一个 3D 球体"
   - "画一个 3D 圆环"
   - "画一个 3D 波浪曲面"

2. 点击"生成图形"按钮

3. AI 会将你的想法转化为数学方程，并自动绘制出图形

📖 **查看 [3D_GUIDE.md](3D_GUIDE.md) 了解更多 3D 绘图技巧！**

## 🏗️ 项目结构

```
You Say I Draw/
├── app.py                    # Streamlit 主应用
├── config/
│   └── settings.py           # 配置管理
├── core/
│   ├── llm_client.py         # LLM API 客户端
│   ├── code_executor.py      # 沙箱代码执行器
│   └── prompt_builder.py     # 系统提示词
├── utils/
│   └── validators.py         # 验证工具
├── tests/
│   └── test_executor.py      # 安全性测试
└── requirements.txt          # Python 依赖
```

## 🔒 安全性

本项目使用多层安全防护：

- ✅ 命名空间隔离（仅允许 numpy 和 matplotlib）
- ✅ 危险代码模式黑名单
- ✅ 代码长度限制
- ✅ 异常捕获与资源清理
- ✅ 输入验证

## 🧪 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行安全性测试
pytest tests/test_executor.py -v
```

## 📋 技术栈

- **前端框架**: Streamlit
- **数学渲染**: NumPy + Matplotlib
- **LLM 集成**: OpenAI API / Google Gemini API
- **配置管理**: Pydantic + python-dotenv
- **测试框架**: pytest

## 🎯 原理

1. 用户输入提示词（如"画一个笑脸"）
2. 系统提示词约束 LLM 输出纯 Python 代码
3. LLM 生成参数方程代码（如 `x = cos(t)`, `y = sin(t)`）
4. 在沙箱环境中安全执行代码
5. Matplotlib 渲染数学图形
6. Streamlit 展示给用户

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License

## 🎓 教育用途

本项目设计用于教学目的，展示了：
- LLM 提示词工程
- 安全的动态代码执行
- Streamlit 应用开发
- 数学可视化

---

**Happy Pi Day! 🥧**
