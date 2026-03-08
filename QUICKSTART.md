# 🥧 你说我画 - 快速启动指南

## ✅ 环境已就绪！

你的项目环境 `you-say-i-draw` 已经成功创建并安装了所有依赖。

## 🚀 快速启动步骤

### 方法 1：使用启动脚本（推荐）

#### Windows 用户：
1. 双击 `setup.bat` 完成环境配置（仅第一次需要）
2. 编辑 `.env` 文件，填入你的 API 密钥
3. 双击 `start.bat` 启动应用

#### Linux/Mac 用户：
```bash
# 第一次运行时
bash setup.sh

# 编辑 .env 文件
nano .env

# 启动应用
bash start.sh
```

### 方法 2：手动启动

```bash
# 1. 激活 conda 环境
conda activate you-say-i-draw

# 2. 配置 API 密钥（如果还没有配置）
# 编辑 .env 文件，填入你的 OpenAI 或 Gemini API 密钥

# 3. 启动 Streamlit 应用
streamlit run app.py
```

## ⚙️ 配置 API 密钥

编辑项目根目录下的 `.env` 文件：

### 使用 OpenAI（推荐）：
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-你的实际密钥
MODEL_NAME=gpt-4
TEMPERATURE=0.7
```

### 使用 Google Gemini：
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=你的实际密钥
MODEL_NAME=gemini-pro
TEMPERATURE=0.7
```

## 🎮 使用方法

1. 启动应用后，浏览器会自动打开 `http://localhost:8501`
2. 在输入框中输入你的想象，例如：
   - "画一个笑脸"
   - "画一个心形"
   - "画一个愤怒的包子"
3. 点击"生成图形"按钮
4. AI 会将你的想法转化为数学方程并自动绘制

## 🧪 运行测试

验证安全性和功能正常：

```bash
# 激活环境
conda activate you-say-i-draw

# 运行所有测试
pytest tests/test_executor.py -v

# 运行特定测试
pytest tests/test_executor.py::TestCodeExecutorSecurity -v
```

## 📊 测试状态

✅ **核心安全功能已验证通过：**
- ✅ 阻止 import 语句
- ✅ 阻止 eval/exec 利用
- ✅ 阻止文件操作
- ✅ 阻止系统模块访问
- ✅ 允许合法的 matplotlib 代码
- ✅ 处理语法错误和运行时错误

## 🛠️ 故障排查

### 问题1：找不到 streamlit 命令
```bash
# 确保激活了正确的环境
conda activate you-say-i-draw

# 或使用完整路径
D:\Anaconda\envs\you-say-i-draw\Scripts\streamlit.exe run app.py
```

### 问题2：API 密钥错误
- 检查 `.env` 文件是否存在
- 确认 API 密钥格式正确
- OpenAI 密钥格式：`sk-...`
- Gemini 密钥：在 Google AI Studio 获取

### 问题3：中文显示乱码
应用已配置中文字体支持（SimHei），Windows 系统通常不会有问题。

## 📝 项目结构

```
You Say I Draw/
├── app.py                 # 主应用（启动这个）
├── config/                # 配置管理
├── core/                  # 核心逻辑
│   ├── code_executor.py   # 沙箱执行器
│   ├── llm_client.py      # LLM 客户端
│   └── prompt_builder.py  # 提示词构建
├── utils/                 # 工具函数
├── tests/                 # 测试文件
├── .env                   # API 密钥配置（需要手动创建）
├── setup.bat              # Windows 安装脚本
└── start.bat              # Windows 启动脚本
```

## 🎯 下一步

1. **首次使用**：配置 .env 文件中的 API 密钥
2. **启动应用**：运行 `start.bat` 或 `streamlit run app.py`
3. **开始创作**：在网页中输入你的想象，让 AI 画图！

## 🎓 示例提示词

尝试这些有趣的提示词：

- **基础图形**：
  - 画一个圆
  - 画一个五角星
  - 画一个正弦波

- **有趣的图案**：
  - 画一个笑脸
  - 画一个心形
  - 画一朵花

- **创意挑战**：
  - 画一个愤怒的包子
  - 画一只蝴蝶
  - 画一个螺旋星系
  - 画一朵玫瑰花

---

**祝你 Pi Day 快乐！🥧**

需要帮助？查看 README.md 或检查代码中的注释。
