# API 配置指南

## 支持的 LLM 服务

本应用支持多种 LLM 服务，包括官方 API 和兼容 OpenAI 格式的第三方服务。

---

## 配置方式

编辑项目根目录的 `.env` 文件。

### 1. OpenAI 官方 API

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key-here
MODEL_NAME=gpt-4
# OPENAI_BASE_URL 留空使用官方地址
```

**说明：**
- 适用于拥有 OpenAI 官方 API 密钥的用户
- 模型选择：`gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`

---

### 2. DeepSeek API（推荐国内用户）

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-deepseek-key-here
MODEL_NAME=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com
```

**说明：**
- DeepSeek 使用 OpenAI 兼容接口
- 注册地址：https://platform.deepseek.com
- 性价比高，适合国内用户
- 支持中文，响应速度快

---

### 3. 其他 OpenAI 兼容服务

支持任何兼容 OpenAI API 格式的服务：

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
MODEL_NAME=model-name
OPENAI_BASE_URL=https://your-api-endpoint.com
```

**兼容服务示例：**
- **Azure OpenAI**: `https://your-resource.openai.azure.com/openai/deployments/your-deployment`
- **Cloudflare AI Gateway**: `https://gateway.ai.cloudflare.com/v1/your-account/your-gateway/openai`
- **本地模型（Ollama等）**: `http://localhost:11434/v1`
- **代理服务**: 任何提供 OpenAI 兼容接口的代理

---

### 4. Google Gemini API

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key-here
MODEL_NAME=gemini-pro
# GEMINI_BASE_URL 通常不需要配置
```

**说明：**
- 适用于 Google AI Studio 用户
- 获取密钥：https://makersuite.google.com/app/apikey
- 免费额度较大

---

## 高级配置

### 使用代理服务

如果需要通过代理访问 API：

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
MODEL_NAME=gpt-4
OPENAI_BASE_URL=https://your-proxy-service.com/v1
```

### 本地部署模型

使用 Ollama 等本地模型服务：

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=ollama  # 可以是任意值
MODEL_NAME=llama2      # 本地模型名称
OPENAI_BASE_URL=http://localhost:11434/v1
```

**注意：** 确保本地服务已启动并支持 OpenAI 兼容接口。

---

## 其他参数说明

### TEMPERATURE
控制生成的随机性：
- `0.0` - 最确定性，适合需要精确输出
- `0.7` - 平衡创意和准确性（推荐）
- `1.0` - 更具创意
- `2.0` - 高度随机

```bash
TEMPERATURE=0.7
```

### MAX_TOKENS
限制生成的最大 token 数：
- 代码生成建议：`1000-2000`
- 复杂图形：`2000-4000`
- 如果代码被截断，可以适当增加

```bash
MAX_TOKENS=2000
```

### TIMEOUT_SECONDS
代码执行超时时间（秒）：
- 简单图形：`5`
- 复杂图形：`10-15`

```bash
TIMEOUT_SECONDS=5
```

---

## 常见问题

### Q: 如何选择合适的服务？

| 服务 | 优势 | 适合人群 |
|-----|------|---------|
| OpenAI 官方 | 质量最高 | 有官方 API 的用户 |
| DeepSeek | 性价比高，速度快 | 国内用户 |
| Gemini | 免费额度大 | 个人开发者 |
| 本地模型 | 隐私保护，无成本 | 有本地算力的用户 |

### Q: DeepSeek 和 OpenAI 有什么区别？

- **DeepSeek**: 国内服务，访问快，价格低，中文友好
- **OpenAI**: 国际服务，需要科学上网，质量稍高

### Q: 可以同时配置多个服务吗？

不可以，每次只能使用一个 `LLM_PROVIDER`。如需切换，修改 `.env` 中的 `LLM_PROVIDER` 即可。

### Q: BASE_URL 是必填的吗？

- **OpenAI 官方**：不需要填写（留空）
- **DeepSeek**：必须填写 `https://api.deepseek.com`
- **其他服务**：根据服务商文档填写

---

## 完整配置示例

### 示例 1：使用 DeepSeek（推荐国内用户）

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai

# API Keys
OPENAI_API_KEY=sk-633471837bdc4cbaa6803167ee050b1d
GEMINI_API_KEY=

# Model Configuration
MODEL_NAME=deepseek-chat
TEMPERATURE=0.7
MAX_TOKENS=2000

# API Base URL
OPENAI_BASE_URL=https://api.deepseek.com
GEMINI_BASE_URL=

# Execution Settings
TIMEOUT_SECONDS=5
MAX_CODE_LENGTH=10000

# App Settings
DEBUG_MODE=false
```

### 示例 2：使用 OpenAI 官方

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-real-openai-key
MODEL_NAME=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=1000
OPENAI_BASE_URL=
```

### 示例 3：使用 Google Gemini

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
MODEL_NAME=gemini-pro
TEMPERATURE=0.7
MAX_TOKENS=1000
```

---

## 获取 API 密钥

### OpenAI
1. 访问 https://platform.openai.com/api-keys
2. 登录或注册账号
3. 创建新的 API 密钥

### DeepSeek
1. 访问 https://platform.deepseek.com
2. 注册账号
3. 在控制台创建 API 密钥

### Gemini
1. 访问 https://makersuite.google.com/app/apikey
2. 使用 Google 账号登录
3. 创建 API 密钥

---

**提示：** 配置完成后，重启应用即可生效！
