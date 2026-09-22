# 启动检查清单（忘了就翻这个）

## 启动前：确认 3 件事

| # | 检查什么 | 怎么查 |
|---|---|---|
| 1 | MySQL 服务在运行 | 打开 Navicat 能连上 → 就是在运行；连不上就 `Win+R` 输入 `services.msc` 启动 MySQL80 |
| 2 | 端口没被占用 | 上一次的服务没关干净？见文末"排错" |
| 3 | 站在正确的目录 | 每个命令都有自己的"家"，见下面 |

> **核心概念**：这个项目是**两个独立的服务**，所以要**开两个终端**，各跑一个，两个都开着才行。

---

## 第一步：启动后端（终端 1）

```powershell
cd D:\memo_backend\fitness\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```

**命令拆解**：`.\venv\Scripts\python.exe`（用项目的 Python）→ `-m uvicorn`（跑 uvicorn）→
`app.main:app`（启动 app/main.py 里的 app）→ `--reload`（改代码自动重启）→ `--port 8001`（端口）

### ✅ 成功的样子

```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 验证：浏览器打开 http://127.0.0.1:8001/docs
能看到"Fitlog健身日志 API"的接口文档 = 后端 OK。**这个终端不要关**。

---

## 第二步：启动前端（终端 2，新开一个）

```powershell
cd D:\memo_backend\fitness\web
npm run dev
```

（`npm run dev` 会去 `package.json` 里找 `"dev": "vite"`，所以必须在 `web\` 目录里执行）

### ✅ 成功的样子

```
  VITE v8.x.x  ready in 300 ms
  ➜  Local:   http://localhost:5174/
```

### 验证：浏览器打开 http://localhost:5174
能看到登录页 = 前端 OK。

---

## 第三步：使用

浏览器访问 **http://localhost:5174**，用 `tester01` / `123456` 登录（或自己注册）。

---

## 停止服务

在**对应的终端窗口**里按 `Ctrl + C`（两个终端各按一次）。

---

## 为什么要开两个终端？

```
终端1: uvicorn  →  监听 8001 端口，提供数据接口（后厨）
终端2: vite     →  监听 5174 端口，提供网页界面（前台）
浏览器访问 5174 → 页面里的请求经 vite 代理转发到 8001 → 拿到数据
```

两个都必须开着。少一个：
- 只开前端 → 页面能打开，但登录/列表全部失败（拿不到数据）
- 只开后端 → 网页打不开（5174 没人服务），但 /docs 能用

---

## 排错速查

| 报错 | 原因 | 解决 |
|---|---|---|
| `ENOENT ... package.json` | 不在 web 目录 | `cd D:\memo_backend\fitness\web` |
| `No module named fastapi` | 用了全局 python | 用 `.\venv\Scripts\python.exe`（或 dev.bat） |
| `WinError 10013` / 端口占用 | 上次的服务没关 | `netstat -ano \| findstr :8001` 找到 PID → `taskkill /PID 号码 /F` |
| 页面能开但数据不显示 | 后端没启动 | 启动终端 1 |
| 中文乱码 | 终端编码 | `chcp 65001` |
| 登录报"用户名或密码错误" | 账号不存在 | 先注册一个 |

---

## 改代码后要重启吗？

| 改了什么 | 要重启吗 |
|---|---|
| Vue 页面（`web/src/...`） | ❌ 不用，Vite 自动热更新 |
| Python 后端（`backend/app/...`） | ❌ 不用，`--reload` 自动重载 |
| `.env` 配置文件 | ✅ 要重启后端 |
| 加了数据库字段（`models.py`） | ✅ 要跑一次 `init_db.py` |
