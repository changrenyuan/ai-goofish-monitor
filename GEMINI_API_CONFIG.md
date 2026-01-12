# Google Gemini API 配置指南

## 🔑 你提供的 API 调用

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AIzaSyAeM0SBO7GlbPmLGrCYq7NqD6fy1SSZpEw' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'
```

这是 Google Gemini 的**原生 API 格式**，但是项目使用的是 **OpenAI 兼容格式**。

---

## 📝 配置到项目的方法

### 步骤 1：获取 Google AI API Key

1. 访问：https://aistudio.google.com/app/apikey
2. 登录 Google 账号
3. 创建 API Key
4. 复制 API Key

**⚠️ 安全提示**：不要在生产环境中使用公开的 API Key！

---

### 步骤 2：配置 .env 文件

打开 `D:\git\ai-goofish-monitor\.env` 文件，配置以下内容：

```bash
# --- AI 模型配置 ---
# Google AI API Key（替换为你自己的）
OPENAI_API_KEY="AIzaSyAeM0SBO7GlbPmLGrCYq7NqD6fy1SSZpEw"

# Google Gemini 的 OpenAI 兼容 API 端点
OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"

# 模型名称（Gemini 2.0 Flash）
OPENAI_MODEL_NAME="gemini-2.0-flash-exp"

# 其他配置
ENABLE_RESPONSE_FORMAT=true
ENABLE_THINKING=false
```

---

### 步骤 3：测试 API 连接

在 CMD 中运行：

```cmd
cd D:\git\ai-goofish-monitor
.venv\Scripts\activate
python -c "from src.infrastructure.config.settings import settings; print(f'API Key: {settings.openai_api_key[:10]}...'); print(f'Base URL: {settings.openai_base_url}'); print(f'Model: {settings.openai_model_name}')"
```

---

## 🔧 API 配置选项

### 推荐的 Gemini 模型

| 模型名称 | 特点 | 适用场景 |
|---------|------|---------|
| `gemini-2.0-flash-exp` | 最快，支持多模态 | **推荐用于本项目**（图片分析 + 文本） |
| `gemini-1.5-pro` | 稳定，多模态 | 如果 Flash 不可用 |
| `gemini-1.5-flash` | 快速，多模态 | 备选方案 |
| `gemini-pro` | 仅文本 | 不推荐（需要图片分析） |

### 配置示例

#### 方案 1：使用 Gemini 2.0 Flash（推荐）

```bash
OPENAI_API_KEY="your-google-api-key"
OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
OPENAI_MODEL_NAME="gemini-2.0-flash-exp"
ENABLE_RESPONSE_FORMAT=true
```

#### 方案 2：使用 Gemini 1.5 Pro

```bash
OPENAI_API_KEY="your-google-api-key"
OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
OPENAI_MODEL_NAME="gemini-1.5-pro"
ENABLE_RESPONSE_FORMAT=true
```

---

## ⚠️ 注意事项

### 1. API Key 安全

❌ **不要**：
- 将 API Key 提交到 Git
- 在公开代码中使用公开 Key
- 分享你的 API Key

✅ **应该**：
- 使用环境变量或 `.env` 文件
- 定期更换 API Key
- 设置使用限额和限制

### 2. 费用

Google Gemini API 有免费额度：
- Gemini 1.5 Flash：每天 15 次/分钟
- Gemini 1.5 Pro：每天 15 次/分钟
- 超出后按使用量计费

查看配额：https://aistudio.google.com/app/apikey

### 3. 多模态支持

本项目需要 AI 分析商品图片，确保选择的模型支持：
- ✅ Gemini 2.0 Flash：支持
- ✅ Gemini 1.5 Pro：支持
- ❌ Gemini Pro：不支持（仅文本）

---

## 🧪 测试 API 连接

### 方法 1：使用 Python 脚本测试

创建测试文件 `test_api.py`：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash-exp",
    messages=[
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ]
)

print(response.choices[0].message.content)
```

运行：
```cmd
python test_api.py
```

### 方法 2：使用 curl 测试

```bash
curl https://generativelanguage.googleapis.com/v1beta/openai/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer AIzaSyAeM0SBO7GlbPmLGrCYq7NqD6fy1SSZpEw' \
  -X POST \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

---

## 🌐 其他 AI 服务提供商

如果你想使用其他 AI 服务，可以参考：

### OpenAI
```bash
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="https://api.openai.com/v1/"
OPENAI_MODEL_NAME="gpt-4o"
```

### DeepSeek
```bash
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="https://api.deepseek.com/v1"
OPENAI_MODEL_NAME="deepseek-chat"
```

### Claude（通过第三方代理）
```bash
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="https://your-proxy-url/v1"
OPENAI_MODEL_NAME="claude-3-5-sonnet"
ENABLE_RESPONSE_FORMAT=true
```

### 豆包（火山引擎）
```bash
OPENAI_API_KEY="..."
OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/v3/"
OPENAI_MODEL_NAME="ep-..."
ENABLE_RESPONSE_FORMAT=false  # 豆包不支持 JSON 响应格式
```

---

## 📚 完整配置示例

```bash
# .env 文件完整配置

# --- AI 模型配置 ---
OPENAI_API_KEY="AIzaSyAeM0SBO7GlbPmLGrCYq7NqD6fy1SSZpEw"
OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
OPENAI_MODEL_NAME="gemini-2.0-flash-exp"

# --- Web 服务配置 ---
SERVER_PORT=5000
WEB_USERNAME=admin
WEB_PASSWORD=admin123

# --- 爬虫配置 ---
RUN_HEADLESS=true
LOGIN_IS_EDGE=false
PCURL_TO_MOBILE=true

# --- 代理配置（可选）---
PROXY_URL=""

# --- 通知配置（可选）---
NTFY_TOPIC_URL=""
BARK_URL=""
WX_BOT_URL=""
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""

# --- 调试配置 ---
AI_DEBUG_MODE=false
ENABLE_THINKING=false
ENABLE_RESPONSE_FORMAT=true
```

---

## ✅ 验证配置

配置完成后，启动服务并测试：

```cmd
cd D:\git\ai-goofish-monitor
start.bat
```

访问 Web 界面：
1. 打开 http://localhost:5000
2. 登录：admin/admin123
3. 进入 **系统设置** → **状态检查**
4. 查看 AI 连接状态

如果显示 "✓ AI 服务连接正常"，说明配置成功！

---

## 🆘 常见问题

### 问题 1：API 调用失败

**错误**：`Error: 403 API key not valid`

**解决**：
- 检查 API Key 是否正确
- 确认 API Key 已启用 Gemini API
- 检查是否有使用限制

### 问题 2：无法分析图片

**错误**：`Error: Model does not support image input`

**解决**：
- 确保使用支持多模态的模型（如 `gemini-2.0-flash-exp`）
- 检查 `ENABLE_RESPONSE_FORMAT` 设置

### 问题 3：响应格式错误

**错误**：`Error: Response format not supported`

**解决**：
```bash
# Gemini 支持
ENABLE_RESPONSE_FORMAT=true

# 豆包不支持
ENABLE_RESPONSE_FORMAT=false
```

---

## 📞 获取帮助

- Google AI Studio: https://aistudio.google.com/
- Gemini API 文档: https://ai.google.dev/gemini-api/docs
- OpenAI 兼容 API: https://ai.google.dev/gemini-api/docs/openai
