# Windows + PyCharm 部署指南

本指南将手把手教你在 Windows 系统上使用 PyCharm 部署 ai-goofish-monitor 项目。

## 📋 前置要求

### 1. 安装必要软件

#### Python（必须）
- 下载：https://www.python.org/downloads/
- 版本：Python 3.10 或更高（推荐 3.11 或 3.12）
- **重要**：安装时勾选 "Add Python to PATH"

#### PyCharm（推荐使用）
- 下载：https://www.jetbrains.com/pycharm/download/
- 推荐版本：PyCharm Community（免费）或 Professional
- 安装后确保 Python 解释器配置正确

#### Node.js（必须，用于前端构建）
- 下载：https://nodejs.org/
- 版本：LTS 版本（18.x 或 20.x）
- 安装后验证：在 CMD 中输入 `node --version` 和 `npm --version`

#### Git（可选，用于克隆）
- 下载：https://git-scm.com/download/win
- 安装选项可全部默认

---

## 🚀 方法一：从 GitHub 克隆（推荐）

### 步骤 1：克隆项目

#### 方式 A：使用 Git（推荐）
在 CMD 或 PowerShell 中运行：
```bash
cd D:\projects  # 或你喜欢的目录
git clone https://github.com/changrenyuan/ai-goofish-monitor.git
cd ai-goofish-monitor
```

#### 方式 B：直接下载 ZIP
1. 访问：https://github.com/changrenyuan/ai-goofish-monitor
2. 点击 "Code" → "Download ZIP"
3. 解压到 `D:\projects\ai-goofish-monitor`

---

## 🎯 方法二：使用 PyCharm 打开项目

### 步骤 1：在 PyCharm 中打开项目

1. **打开 PyCharm**
2. 点击 **File** → **Open**
3. 选择 `D:\projects\ai-goofish-monitor` 文件夹
4. 点击 **OK**，等待 PyCharm 索引完成

### 步骤 2：配置 Python 解释器

1. **打开设置**
   - 点击 **File** → **Settings**（或 `Ctrl + Alt + S`）

2. **配置解释器**
   - 左侧导航：**Project: ai-goofish-monitor** → **Python Interpreter**
   - 点击右上角 **Add Interpreter** → **New Conda Environment** 或 **New Virtualenv Environment**

3. **创建虚拟环境**
   - Location: `D:\projects\ai-goofish-monitor\.venv`
   - Base interpreter: 选择 Python 3.11 或 3.12
   - 点击 **Create**，等待虚拟环境创建完成

### 步骤 3：安装 Python 依赖

#### 方式 A：使用 PyCharm 界面（推荐新手）
1. 打开 **Terminal**（`Alt + F12`）
2. 确保虚拟环境已激活（命令行前面应该有 `(.venv)`）
3. 运行：
   ```bash
   pip install -r requirements.txt
   ```

#### 方式 B：使用命令行
1. 在 CMD 或 PowerShell 中：
   ```bash
   cd D:\projects\ai-goofish-monitor
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 步骤 4：安装 Playwright 浏览器

在 PyCharm Terminal 中运行：
```bash
playwright install chromium
```

> ⚠️ **Windows 用户注意**：首次运行可能需要几分钟下载浏览器。

### 步骤 5：构建前端

在 PyCharm Terminal 中运行：
```bash
cd web-ui
npm install
npm run build
cd ..
```

> 📝 说明：
> - `npm install` 会下载前端依赖（需要 2-5 分钟）
> - `npm run build` 会构建前端静态文件到 `dist/` 目录

### 步骤 6：配置环境变量

#### 方法 A：复制示例配置（推荐）
在 PyCharm Terminal 中运行：
```bash
copy .env.example .env
copy config.json.example config.json
```

#### 方法 B：手动创建
1. 在项目根目录创建 `.env` 文件
2. 在项目根目录创建 `config.json` 文件
3. 复制 `.env.example` 和 `config.json.example` 的内容

#### 配置 `.env` 文件（必填）
```bash
# --- AI 模型配置 ---
OPENAI_API_KEY="your-api-key-here"        # 必填：你的 AI API Key
OPENAI_BASE_URL="https://api.openai.com/v1"  # 必填：API 地址
OPENAI_MODEL_NAME="gpt-4o"               # 必填：模型名称

# --- Web 服务配置 ---
SERVER_PORT=5000                          # 服务端口
WEB_USERNAME=admin                       # Web 登录用户名
WEB_PASSWORD=admin123                     # Web 登录密码

# --- 其他配置（可选）---
RUN_HEADLESS=true                         # 是否无头模式运行
NTFY_TOPIC_URL=""                         # ntfy 通知地址（可选）
```

> 💡 **提示**：在 PyCharm 中打开 `.env` 文件，右键选择 **Open as Text** 即可编辑。

### 步骤 7：创建运行配置

1. **打开 Run Configuration**
   - 点击右上角下拉菜单 → **Edit Configurations...**

2. **添加 Python 配置**
   - 点击左上角 **+** → **Python**
   - 配置如下：
     - **Name**: `ai-goofish-monitor`
     - **Script path**: 选择 `src/app.py`
     - **Python interpreter**: 选择刚创建的虚拟环境
     - **Environment variables**:
       - 点击 **Environment variables** 后的文件夹图标
       - 点击 **+** 添加：
         - Key: `PYTHONPATH`
         - Value: `D:\projects\ai-goofish-monitor`
     - **Working directory**: `D:\projects\ai-goofish-monitor`

3. **保存配置**
   - 点击 **OK**

---

## ▶️ 运行项目

### 方式 A：使用 PyCharm 运行（推荐）

1. 确保选择了刚创建的 `ai-goofish-monitor` 配置
2. 点击右上角绿色 **▶ Run** 按钮（或 `Shift + F10`）
3. 查看下方 **Run** 窗口的日志输出

### 方式 B：使用命令行运行

在 PyCharm Terminal 中运行：
```bash
cd D:\projects\ai-goofish-monitor
python -m uvicorn src.app:app --host 0.0.0.0 --port 5000
```

### 方式 C：使用 start.sh（需转换为 Windows）

由于 `start.sh` 是 Linux 脚本，Windows 用户请使用上述方式 A 或 B。

---

## 🌐 访问 Web 界面

1. 打开浏览器
2. 访问：http://localhost:5000
3. 输入用户名和密码：
   - 用户名：`admin`
   - 密码：`admin123`

---

## 🔧 配置闲鱼账号

### 步骤 1：安装 Chrome 扩展

1. 在 Chrome 中安装扩展：
   https://chromewebstore.google.com/detail/xianyu-login-state-extrac/eidlpfjiodpigmfcahkmlenhppfklcoa

2. 登录闲鱼网页版

3. 点击扩展图标，复制登录状态 JSON

### 步骤 2：在 Web 界面添加账号

1. 访问 http://localhost:5000
2. 登录后进入 **闲鱼账号管理**
3. 点击 **添加账号**
4. 粘贴复制的 JSON
5. 保存

账号会保存到 `state/` 目录（如 `state/acc_1.json`）

---

## 🐛 常见问题排查

### 问题 1：pip 安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**解决方案**：
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2：npm install 慢或失败

**解决方案**：
```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 问题 3：Playwright 浏览器下载失败

**解决方案**：
```bash
# 设置国内镜像
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 重新安装
playwright install chromium
```

### 问题 4：端口 5000 被占用

**症状**：
```
OSError: [WinError 10048] 只有每个套接字地址
```

**解决方案**：
1. 在 `.env` 文件中修改 `SERVER_PORT=5001`
2. 重新运行服务
3. 或关闭占用 5000 端口的程序

### 问题 5：Python 解释器找不到

**解决方案**：
1. 打开 PyCharm **Settings** → **Project** → **Python Interpreter**
2. 检查解释器路径是否正确
3. 如果显示红色波浪线，点击 **Add Interpreter** 重新配置

### 问题 6：运行时提示 "ModuleNotFoundError"

**症状**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
```bash
# 确保虚拟环境已激活
.venv\Scripts\activate

# 重新安装依赖
pip install -r requirements.txt
```

---

## 📦 后台运行（Windows）

### 使用 PyCharm

直接使用 PyCharm 的 Run 按钮运行即可，关闭 PyCharm 时服务会停止。

### 使用批处理文件

1. 创建文件 `start.bat`：
```batch
@echo off
cd /d D:\projects\ai-goofish-monitor
.venv\Scripts\activate
python -m uvicorn src.app:app --host 0.0.0.0 --port 5000
pause
```

2. 双击运行，关闭 CMD 窗口服务会停止。

### 使用 Pythonw（无窗口）

创建文件 `start_hidden.bat`：
```batch
@echo off
cd /d D:\projects\ai-goofish-monitor
.venv\Scripts\pythonw -m uvicorn src.app:app --host 0.0.0.0 --port 5000
```

注意：这种方式需要在任务管理器中手动结束进程。

---

## 🎓 PyCharm 实用技巧

### 1. 自动格式化代码
- Settings → **Tools** → **Black**
- 勾选 "On save"

### 2. 安装有用的插件
- **Black**: 代码格式化
- **Rainbow Brackets**: 括号颜色高亮
- **Key Promoter X**: 快捷键提示

### 3. 设置断点调试
- 在代码行号左侧点击，设置红色断点
- 点击右上角 🐛 Debug 按钮
- 使用 **F8** 单步执行，**F9** 继续执行

### 4. 查看环境变量
- 在运行配置中已配置 `PYTHONPATH`
- 可在代码中使用：
  ```python
  import os
  print(os.getenv('OPENAI_API_KEY'))
  ```

---

## 📞 获取帮助

如果遇到问题：

1. 查看日志：PyCharm Run 窗口的输出
2. 检查配置：`.env` 和 `config.json` 文件
3. 查看文档：
   - `README.md`: 项目总体说明
   - `VERCEL_DEPLOYMENT.md`: 云平台部署
   - `LOCAL_GUIDE.md`: 本地运行指南

---

## ✅ 部署验证清单

部署完成后，检查以下项目：

- [ ] Python 解释器已配置（3.10+）
- [ ] 虚拟环境已创建并激活
- [ ] 所有 Python 依赖已安装
- [ ] Playwright 浏览器已安装
- [ ] 前端已构建（`dist/` 目录存在）
- [ ] `.env` 文件已创建并配置
- [ ] `config.json` 文件已创建
- [ ] 服务能正常启动
- [ ] 能访问 http://localhost:5000
- [ ] 能登录 Web 界面（admin/admin123）
- [ ] 已添加闲鱼账号（可选）

完成以上所有步骤后，项目已成功部署！🎉
