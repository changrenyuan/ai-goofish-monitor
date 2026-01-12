# 本地部署网页打不开 - 诊断与解决

## 问题症状

服务已启动，但访问 http://localhost:5000 打不开网页。

从日志看服务正常：
```
INFO: Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
应用启动完成
```

---

## 🔍 诊断步骤

### 步骤 1：检查前端是否构建

**最常见的原因**：前端没有构建，`dist/` 目录不存在。

在 CMD 或 PowerShell 中运行：

```cmd
cd D:\git\ai-goofish-monitor
dir dist
```

**如果显示**：
```
找不到文件
```
或
```
系统找不到指定的路径
```

**这就是问题所在！**

**解决方案**：

```cmd
cd D:\git\ai-goofish-monitor\web-ui
npm install
npm run build
cd ..
```

完成后应该看到 `dist\index.html` 文件存在。

---

### 步骤 2：测试健康检查接口

在浏览器或 CMD 中运行：

```cmd
curl http://localhost:5000/health
```

或在浏览器中访问：
```
http://localhost:5000/health
```

**如果返回**：
```json
{"status":"healthy","message":"服务正常运行"}
```

说明后端服务正常。

**如果打不开**：检查端口是否被占用或防火墙问题。

---

### 步骤 3：检查端口是否真的在监听

在 CMD 中运行：

```cmd
netstat -ano | findstr :5000
```

**应该看到类似**：
```
TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING    29292
```

**如果没有输出**：说明服务没有真正启动。

---

### 步骤 4：检查防火墙

Windows Defender 防火墙可能阻止了 5000 端口。

**临时关闭防火墙测试**：

1. 打开 **控制面板** → **Windows Defender 防火墙**
2. 点击左侧 **启用或关闭 Windows Defender 防火墙**
3. 专用网络和公用网络都选择 **关闭**
4. 再次尝试访问 http://localhost:5000

**如果可以访问了**：需要添加防火墙规则

```cmd
netsh advfirewall firewall add rule name="Allow Port 5000" dir=in action=allow protocol=TCP localport=5000
```

---

### 步骤 5：检查浏览器访问的 URL

**正确的访问地址**：
- ✅ `http://localhost:5000`
- ✅ `http://127.0.0.1:5000`
- ❌ `http://0.0.0.0:5000`（这个地址浏览器无法访问）

**注意**：
- 确保使用 `http://` 而不是 `https://`
- 如果设置了用户名密码，需要输入认证信息
  - 用户名：`admin`
  - 密码：`admin123`

---

### 步骤 6：查看浏览器错误信息

打开浏览器的开发者工具（按 F12），查看 **Console** 和 **Network** 标签页。

**常见错误**：
1. `net::ERR_CONNECTION_REFUSED`：服务未启动
2. `net::ERR_CONNECTION_TIMED_OUT`：防火墙阻止或端口被占用
3. `404 Not Found`：前端未构建或 URL 错误
4. `401 Unauthorized`：需要登录认证

---

## 💡 完整解决方案

### 方案一：前端未构建（最常见）

**在 CMD 中运行**：

```cmd
cd D:\git\ai-goofish-monitor\web-ui
npm install
npm run build
```

**等待构建完成**，应该看到：

```
✓ built in X.XXs
```

**验证构建**：

```cmd
cd D:\git\ai-goofish-monitor
dir dist
```

应该看到：
```
dist\
├── assets\
└── index.html
```

然后刷新浏览器 http://localhost:5000

---

### 方案二：修改启动端口

如果 5000 端口被占用，修改 `.env` 文件：

```bash
# 打开 .env 文件
SERVER_PORT=5001
```

重新启动服务，访问：
```
http://localhost:5001
```

---

### 方案三：检查 Python 脚本启动方式

你当前的启动方式：

```cmd
D:\git\ai-goofish-monitor\.venv\Scripts\python.exe D:\git\ai-goofish-monitor\src\app.py
```

**改为使用 uvicorn 启动（推荐）**：

```cmd
cd D:\git\ai-goofish-monitor
.venv\Scripts\activate
python -m uvicorn src.app:app --host 0.0.0.0 --port 5000
```

**或者使用 start.bat**：

```cmd
cd D:\git\ai-goofish-monitor
start.bat
```

---

### 方案四：使用 PyCharm 运行

1. 打开 PyCharm
2. **File** → **Open** → 选择 `D:\git\ai-goofish-monitor`
3. 配置 Run Configuration：
   - **Script path**: `src/app.py`
   - **Python interpreter**: 选择 `.venv\python.exe`
   - **Environment variables**: 添加 `PYTHONPATH=D:\git\ai-goofish-monitor`
4. 点击运行

---

## 📋 快速检查清单

在 CMD 中运行以下命令：

### 1. 检查 dist 目录

```cmd
dir D:\git\ai-goofish-monitor\dist
```

✅ 应该看到 `index.html` 文件

### 2. 检查服务监听

```cmd
netstat -ano | findstr :5000
```

✅ 应该看到 `LISTENING` 状态

### 3. 测试健康检查

```cmd
curl http://localhost:5000/health
```

✅ 应该返回 JSON 响应

### 4. 测试主页

```cmd
curl -u admin:admin123 http://localhost:5000/
```

✅ 应该返回 HTML 内容（或前端构建完成的提示）

---

## 🐛 常见问题

### 问题 1：显示 "前端构建产物不存在"

**原因**：`dist/` 目录不存在或为空

**解决**：
```cmd
cd D:\git\ai-goofish-monitor\web-ui
npm run build
```

### 问题 2：ERR_CONNECTION_REFUSED

**原因**：服务未启动或端口错误

**解决**：
```cmd
# 检查服务是否在运行
netstat -ano | findstr :5000

# 检查进程
tasklist | findstr python

# 重启服务
.venv\Scripts\activate
python -m uvicorn src.app:app --host 0.0.0.0 --port 5000
```

### 问题 3：ERR_CONNECTION_TIMED_OUT

**原因**：防火墙阻止或端口被占用

**解决**：
```cmd
# 临时关闭防火墙测试
# 或添加防火墙规则
netsh advfirewall firewall add rule name="Allow Port 5000" dir=in action=allow protocol=TCP localport=5000
```

### 问题 4：401 Unauthorized

**原因**：需要认证

**解决**：在浏览器中访问时弹出登录框，输入：
- 用户名：`admin`
- 密码：`admin123`

### 问题 5：浏览器一直转圈，不显示任何内容

**原因**：前端 JavaScript 加载失败

**解决**：
```cmd
# 检查 dist/assets 目录
dir D:\git\ai-goofish-monitor\dist\assets

# 如果目录为空，重新构建前端
cd D:\git\ai-goofish-monitor\web-ui
npm run build
```

---

## 🎯 推荐的一键部署流程

### 第一次部署

```cmd
# 1. 进入项目目录
cd D:\git\ai-goofish-monitor

# 2. 运行安装脚本（如果还没运行）
install.bat

# 3. 配置 .env 文件（用记事本打开）
notepad .env
# 修改 OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_NAME

# 4. 启动服务
start.bat
```

### 后续启动

```cmd
# 直接运行启动脚本
cd D:\git\ai-goofish-monitor
start.bat
```

---

## 📞 仍然无法解决？

### 提供以下信息以便进一步诊断：

1. 运行以下命令的输出：

```cmd
cd D:\git\ai-goofish-monitor
dir dist
netstat -ano | findstr :5000
curl http://localhost:5000/health
```

2. 浏览器 F12 打开后的错误信息

3. 完整的服务启动日志

---

## ✅ 预期的正常状态

当一切正常时，你应该能够：

1. 访问 http://localhost:5000/health 看到：
   ```json
   {"status":"healthy","message":"服务正常运行"}
   ```

2. 访问 http://localhost:5000/ 看到：
   - 弹出登录框
   - 输入 admin/admin123
   - 看到 Web 管理界面

3. 在 CMD 中看到：
   ```
   dist\
   ├── assets\
   └── index.html
   ```
