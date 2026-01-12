# Vercel 部署指南

## ⚠️ 重要提示

**ai-goofish-monitor 项目包含 Playwright 浏览器自动化和定时任务，这些功能在 Vercel Serverless 环境中有以下限制：**

1. **Playwright 浏览器**: Vercel Serverless 函数不支持运行 Chromium 浏览器，超时和内存限制会导致失败
2. **定时任务 (APScheduler)**: Serverless 环境无法运行长期的后台进程
3. **持续监控**: 需要长时间运行的爬虫进程与 Serverless 架构不兼容

## 推荐部署平台

### ✅ 推荐方案：Docker + 支持容器的平台

#### 1. Railway.app（推荐）
```bash
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 2. 登录并初始化项目
railway login
railway init
railway up

# 3. 配置环境变量
railway variables set OPENAI_API_KEY="your-key"
railway variables set OPENAI_BASE_URL="your-url"
railway variables set OPENAI_MODEL_NAME="your-model"

# 4. 部署
railway up
```

#### 2. Render.com（推荐 Docker 部署）
```bash
# 1. 推送代码到 GitHub
git add .
git commit -m "Ready for Render"
git push

# 2. 在 Render Dashboard 创建新的 Web Service
# 3. 选择 Dockerfile 构建方式
# 4. 配置环境变量
# 5. 自动部署
```

#### 3. Fly.io
```bash
# 1. 安装 Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. 登录
flyctl auth login

# 3. 启动应用
flyctl launch

# 4. 配置环境变量
flyctl secrets set OPENAI_API_KEY="your-key"
flyctl secrets set OPENAI_BASE_URL="your-url"
flyctl secrets set OPENAI_MODEL_NAME="your-model"

# 5. 部署
flyctl deploy
```

#### 4. 自建 VPS + Docker（最灵活）
```bash
# 1. 在 VPS 上克隆项目
git clone https://github.com/changrenyuan/ai-goofish-monitor.git
cd ai-goofish-monitor

# 2. 使用 Docker Compose 部署
docker compose up -d

# 3. 查看日志
docker compose logs -f app
```

---

## ⚠️ Vercel 部署（仅限 API）

如果你仍想部署到 Vercel，**仅能使用 Web UI 和基本 API 功能，无法使用爬虫和定时任务**。

### 部署步骤

#### 1. 修改 `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

#### 2. 配置环境变量
在 Vercel Dashboard 中添加以下环境变量：
- `OPENAI_API_KEY`: 你的 AI API Key
- `OPENAI_BASE_URL`: AI API 地址
- `OPENAI_MODEL_NAME`: 模型名称
- `WEB_USERNAME`: Web 用户名（默认 admin）
- `WEB_PASSWORD`: Web 密码（默认 admin123）

#### 3. 部署到 Vercel
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

#### 4. 注意事项
- ✅ 可以使用 Web UI 界面
- ✅ 可以进行基本的数据查询
- ❌ **无法**使用闲鱼爬虫功能
- ❌ **无法**使用定时任务
- ❌ **无法**使用实时监控

---

## 为什么推荐 Docker 部署

| 功能 | Vercel | Docker (Railway/Render/Fly) |
|------|--------|----------------------------|
| Playwright 浏览器 | ❌ 不支持 | ✅ 完全支持 |
| 定时任务 | ❌ 不支持 | ✅ 完全支持 |
| 长时间运行 | ❌ 60秒超时 | ✅ 无限制 |
| WebSocket | ❌ 受限 | ✅ 完全支持 |
| 文件系统 | ❌ 只读 | ✅ 完全支持 |
| 环境变量 | ✅ 支持 | ✅ 支持 |
| 域名绑定 | ✅ 免费 | ✅ 支持（部分付费） |

---

## 快速开始：使用 Railway 部署（最简单）

```bash
# 1. 一键部署到 Railway
railway init --from https://github.com/changrenyuan/ai-goofish-monitor

# 2. 配置环境变量
railway variables set OPENAI_API_KEY="sk-..."
railway variables set OPENAI_BASE_URL="https://..."
railway variables set OPENAI_MODEL_NAME="gpt-4o"

# 3. 部署
railway up

# 4. 获取访问地址
railway domain
```

---

## 故障排除

### 问题 1: Vercel 构建失败
**错误**: `Project is missing a [project] table`

**解决**: 已修复 `pyproject.toml`，添加了 `[project]` 表和依赖信息。

### 问题 2: Playwright 安装失败
**原因**: Vercel Serverless 环境不支持安装浏览器

**解决**: 使用 Docker 部署到支持容器的平台

### 问题 3: 定时任务不工作
**原因**: Vercel 函数执行完成后进程会被终止

**解决**: 使用 Railway/Render 等支持长期运行的容器平台

---

## 总结

| 需求 | 推荐平台 |
|------|---------|
| 完整功能（爬虫+定时任务） | Railway, Render, Fly.io, 自建 VPS |
| 仅 API 和 Web UI | Vercel, Netlify Functions |
| 低成本/免费额度 | Railway ($5 免费额度), Render (免费层) |
| 最简单部署 | Railway (一键部署) |
| 国内访问友好 | 阿里云, 腾讯云 + Docker |

**强烈建议使用 Railway 或 Render 进行完整功能部署。**
