# 后续练习清单（如果你想自己动手）

项目主体我已经写完了（按你"仿照 ai_emotion 给我写"的要求）。
但**看懂 ≠ 会写**，所以这里留几个"小改动"给你练手，难度从低到高。

## 🟢 低难度（改几行就能看到效果）

1. **改默认值**：`web/src/views/record.vue` 里 `weight` / `reps` 的默认值改成你自己常用的
2. **改文案**：应用名集中在 `web/src/config/index.js` 的 `APP_NAME`（当前是 Fitlog健身日志），
   改完页面导航栏和登录页标题都会变
3. **加校验**：给"添加动作"弹窗加规则——动作名不能超过 10 个字

## 🟡 中难度（照抄现有模式即可）

4. **加"备注"字段**：`set_logs` 加一列 `note`（比如"力竭"），
   需要同时改：`models.py` → `schemas.py` → `routers/exercises.py` → `record.vue`
   （⚠️ 加列后要重建表，或在 Navicat 里手动加列）
5. **组间休息倒计时**：记录成功后启动 90 秒倒计时（`setInterval` + `onUnmounted` 清理）
6. **动作排序**：让列表按"今日是否练过"排序（练过的排前面）

## 🔴 高难度（需要自己设计）

7. **训练历史页**：新建 `views/history.vue` + 后端 `GET /api/history?date=2026-09-22`，
   按天展示每个动作做了几组（提示：`func.date(SetLog.created_at)` + `GROUP BY`）
8. **统计图表**：用 ECharts 画"最近 7 天训练量"

## 📌 改完记得提交

```powershell
cd D:\memo_backend
git add .
git commit -m "健身项目：xxxx"
```

---

## 附：项目里每一处对应你学过的什么

| 文件 | 对应知识点 |
|---|---|
| `backend/app/models.py` | SQLAlchemy 模型、外键、一对多关系、级联删除 |
| `backend/app/schemas.py` | Pydantic 校验（Field 的 ge/le/min_length） |
| `backend/app/routers/exercises.py` | FastAPI 路由、依赖注入、HTTPException、GROUP BY、权限校验 |
| `backend/app/response.py` | 异常处理器、统一响应格式 |
| `backend/app/auth.py` | bcrypt 哈希、JWT 签发/解析、APIKeyHeader |
| `web/src/utils/request.js` | axios 实例、请求/响应拦截器、Promise |
| `web/src/router/index.js` | vue-router 嵌套路由、路由守卫 |
| `web/src/stores/user.js` | Pinia 状态管理 |
| `web/src/views/record.vue` | Vue3 组合式 API、ref/computed/onMounted、props |
