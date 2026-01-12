# AI 配置指南

## 问题诊断

如果你遇到以下错误：
```
AI任务生成API发生未知错误: AI客户端未初始化，无法生成分析标准。请检查.env配置。
```

这表示 AI 客户端没有正确初始化，通常是因为 API Key 配置不正确。

## 快速诊断

运行诊断脚本检查配置：

```bash
python diagnose_ai.py
```

诊断脚本会检查：
- .env 文件是否存在
- 必要的环境变量是否配置（OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_NAME）
- API Key 格式是否正确
- AI 客户端是否可以正常初始化

## 解决方案

### 方案 1：使用自动配置工具（推荐）

运行配置工具：
```bash
python configure_ai.py
```

配置工具会引导你：
1. 选择 AI 提供商（Google Gemini、OpenAI、DeepSeek 等）
2. 输入 API Key
3. 选择模型
4. （可选）配置代理

### 方案 2：手动配置

1. 打开 `.env` 文件
2. 找到以下配置项：
   ```env
   OPENAI_API_KEY="your-api-key-here"
   OPENAI_BASE_URL="https://api.openai.com/v1/"
   OPENAI_MODEL_NAME="gpt-4o"
   ```

3. 根据你使用的 AI 提供商，修改这些值：

#### Google Gemini (推荐，免费额度)

1. 访问 https://aistudio.google.com/app/apikey 获取 API Key
2. 配置：
   ```env
   OPENAI_API_KEY="AIzaSyC5..."  # 你的 API Key
   OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   OPENAI_MODEL_NAME="gemini-2.0-flash-exp"  # 或 gemini-2.5-pro, gemini-1.5-pro
   ```

#### OpenAI

1. 访问 https://platform.openai.com/api-keys 获取 API Key
2. 配置：
   ```env
   OPENAI_API_KEY="sk-proj-..."  # 你的 API Key
   OPENAI_BASE_URL="https://api.openai.com/v1/"
   OPENAI_MODEL_NAME="gpt-4o"  # 或 gpt-4o-mini
   ```

#### DeepSeek (不支持图片分析)

1. 访问 https://platform.deepseek.com/api_keys 获取 API Key
2. 配置：
   ```env
   OPENAI_API_KEY="sk-..."  # 你的 API Key
   OPENAI_BASE_URL="https://api.deepseek.com/v1/"
   OPENAI_MODEL_NAME="deepseek-chat"
   ```
   ⚠️ **注意**：DeepSeek 模型不支持图片分析，只能分析文本数据

#### 豆包 (Doubao)

1. 访问 https://console.volcengine.com/ark 获取 API Key
2. 配置：
   ```env
   OPENAI_API_KEY="xxxx-xxxx"  # 你的 API Key
   OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3/"
   OPENAI_MODEL_NAME="doubao-vision"
   ```

### 方案 3：配置代理（可选）

如果你的网络环境无法直接访问 AI 服务，可以配置代理：

```env
PROXY_URL="http://127.0.0.1:7890"  # 或 socks5://127.0.0.1:1080
```

## 验证配置

配置完成后，运行诊断脚本验证：

```bash
python diagnose_ai.py
```

如果所有检查都通过，说明配置成功。

## 常见问题

### Q1: API Key 格式不正确

**错误提示**：
```
❌ API Key: sk-... (占位符，未配置)
```

**解决方法**：
1. 确保你使用了真实的 API Key，而不是示例或占位符
2. 检查 API Key 是否完整，没有被截断
3. 确保从官方渠道获取 API Key

### Q2: 网络连接失败

**错误提示**：
```
❌ AI 客户端不可用
可能的原因：
1. API Key 无效或过期
2. Base URL 配置错误
3. 网络连接问题
4. 代理配置问题
```

**解决方法**：
1. 验证 API Key 是否有效
2. 检查 Base URL 是否正确
3. 如果在中国大陆，可能需要配置代理
4. 尝试使用不同的网络环境（如切换 WiFi/移动数据）

### Q3: 不支持图片分析

如果你使用的是不支持图片分析的模型（如 DeepSeek），你仍然可以使用系统，但：
- 只能分析商品文本信息
- 无法分析商品图片
- AI 分析结果可能不够准确

建议更换支持多模态的模型（如 Gemini、GPT-4o）。

### Q4: API 额度不足

**错误提示**：
```
Error: Quota exceeded
```

**解决方法**：
1. 检查你的 AI 服务账户余额
2. 使用免费的 Gemini API（有每日配额限制）
3. 升级你的付费计划

## 模型推荐

| 模型 | 速度 | 多模态 | 免费 | 推荐度 |
|------|------|--------|------|--------|
| gemini-2.0-flash-exp | ⚡⚡⚡ | ✅ | ✅ | ★★★★★ |
| gemini-2.5-pro | ⚡⚡ | ✅ | ✅ | ★★★★ |
| gemini-1.5-pro | ⚡⚡ | ✅ | ✅ | ★★★★ |
| gemini-1.5-flash | ⚡⚡⚡ | ✅ | ✅ | ★★★ |
| gpt-4o | ⚡⚡ | ✅ | ❌ | ★★★★ |
| gpt-4o-mini | ⚡⚡⚡ | ✅ | ❌ | ★★★ |
| deepseek-chat | ⚡⚡ | ❌ | ✅ | ★★ (不支持图片) |

## 获取帮助

如果仍然无法解决，请：
1. 检查项目 GitHub Issues
2. 查看 LOGS 目录下的日志文件
3. 运行 `python diagnose_ai.py` 获取详细诊断信息
