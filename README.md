# 🏋️ Fitlog健身日志（fitness）

记录健身时每个动作做到第几组的小程序。前后端分离：
**FastAPI（信封格式 API）+ MySQL** 后端，**Vue3 + Element Plus**（Web 版）与 **uni-app**（小程序版）共用同一套后端。

> 本项目的写法**仿照** `C:\Users\jxgm\Desktop\git\ai_emotion`：
> `config/` + `utils/request.js` + `api/` 分层、Element Plus 组件、`@` 别名、Vite 代理、`{code,data,msg}` 响应信封。

---

## 一、目录结构

```
fitness/
├── backend/                        FastAPI 后端（端口 8001）
│   ├── app/
│   │   ├── config.py               配置（读 .env）
│   │   ├── database.py             engine / SessionLocal / Base
│   │   ├── models.py               三张表：users / exercises / set_logs
│   │   ├── schemas.py              请求/响应数据格式（Pydantic）
│   │   ├── auth.py                 密码哈希 + JWT + 守门员 get_current_user
│   │   ├── response.py             ⭐ 统一信封 {code,data,msg} + 异常处理
│   │   ├── main.py                 入口：挂路由、CORS、异常处理
│   │   └── routers/
│   │       ├── auth.py             注册/登录/我是谁
│   │       └── exercises.py        动作增删查 + 组记录增删查
│   ├── init_db.py                  建表脚本
│   ├── smoke_test.py               后端冒烟测试（22 项）
│   ├── dev.bat                     一键启动
│   └── .env                        数据库地址、JWT 密钥
│
└── web/                            Vue3 网页版（端口 5174）
    ├── vite.config.js              @ 别名 + /api 代理到 8001
    └── src/
        ├── config/index.js         应用名、API 前缀
        ├── utils/request.js        ⭐ axios 封装（带 token + 拆信封 + 统一报错）
        ├── api/fitness.js          所有接口函数
        ├── router/index.js         路由表 + 登录守卫
        ├── stores/user.js          Pinia：登录状态
        ├── components/             AuthLayout（登录页布局）/ FrontendLayout（主布局）
        └── views/                  login / register / home / record
```

---

## 二、怎么跑起来（手动命令，不用脚本）

**终端 1（后端，端口 8001）**
```powershell
cd D:\memo_backend\fitness\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```
→ 文档 http://127.0.0.1:8001/docs

**终端 2（前端，端口 5174）**
```powershell
cd D:\memo_backend\fitness\web
npm run dev
```
→ 打开 http://localhost:5174

> ⚠️ `npm run dev` 必须在**有 package.json 的目录**（也就是 `web\`）里执行，
> 在 `fitness\` 或 `backend\` 里执行会报 `ENOENT ... package.json`。

> 测试账号（冒烟测试建的）：`tester01` / `123456`，也可以自己注册。

---

## 三、后端 API（全部返回 `{code, data, msg}`）

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录，data = `{token, userInfo}` |
| GET | `/api/auth/me` | 当前用户 |
| GET | `/api/exercises` | 我的动作（带 `today_sets` 今日组数） |
| POST | `/api/exercises` | 添加动作 `{name, target_sets}` |
| DELETE | `/api/exercises/{id}` | 删除动作（组记录级联删除） |
| GET | `/api/exercises/{id}/sets` | 该动作的组记录 |
| POST | `/api/exercises/{id}/sets` | ⭐ 记录一组 `{weight, reps}`，**组号后端自动算** |
| DELETE | `/api/sets/{id}` | 撤销一组 |

### 响应信封约定

```json
成功：{ "code": "200", "data": { ... }, "msg": "success" }
登录失效：{ "code": "-1", "data": null, "msg": "登录已过期，请重新登录" }
业务错误：{ "code": "400", "data": null, "msg": "这个动作已经有了" }
参数错误：{ "code": "422", ... }   找不到：{ "code": "404", ... }   无权限：{ "code": "403", ... }
```

⚠️ 注意：用信封格式后 **HTTP 状态码永远是 200**，成功/失败看 body 里的 `code`。
这是很多公司（尤其 Java 系）的约定，代价是不如 REST 直观。前端 `request.js` 里那段"拆信封"就是配合它的。

---

## 四、关键设计点（面试/复习能用）

1. **"第几组"由后端算**：`set_number = max(已有组号) + 1`。
   为什么不让前端传？——前端可以随便编数字，后端是唯一可信来源。用 `max` 而不是 `count`，是为了删掉中间某组后不撞号。
2. **所有查询都带 `user_id == current_user.id`**：数据隔离的安全底线，不写就能看到别人的数据。
3. **今日组数用 `GROUP BY` 一次查出**：避免在循环里反复查数据库（N+1 问题）。
4. **级联删除**：`relationship(cascade="all, delete-orphan")`，删动作时它的组记录一起删。
5. **令牌放请求头 `token`**：`auth.py` 用 `APIKeyHeader(name="token")`；前端拦截器自动加。
6. **跨域用 Vite 代理**而不是后端 CORS：前端请求 `/api/xxx` 被 Vite 转发到 8001，浏览器以为是同源。

---

## 五、学习地图：想看懂代码，按这个顺序读

1. `web/src/utils/request.js` —— 一个请求从发出到拿数据的全过程（token、信封、报错）
2. `web/src/api/fitness.js` —— 接口怎么组织
3. `web/src/views/record.vue` —— 页面"拉数据 → 渲染 → 提交 → 刷新"的标准套路
4. `backend/app/routers/exercises.py` —— 后端接口的标准骨架（查/判断/抛错/返回）
5. `backend/app/response.py` —— 信封格式是怎么统一的
6. `backend/app/auth.py` —— 登录态是怎么被认出来的

---

## 六、下一步

- [ ] **uni-app 版**：同一套后端，做小程序版（H5 调试 → 微信开发者工具）
- [ ] 组间休息倒计时（纯前端逻辑，练 `setInterval` + 状态管理）
- [ ] 历史记录页（按天看训练，练 `GROUP BY` 日期）
- [ ] 训练统计图表（ECharts）
- [ ] 移除测试数据：`DELETE FROM set_logs; DELETE FROM exercises; DELETE FROM users;`
