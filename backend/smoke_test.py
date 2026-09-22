# fitness/backend/smoke_test.py
# 后端冒烟测试：把整个"信封格式"链路跑一遍
# 用法：.\venv\Scripts\python.exe smoke_test.py   （需要后端已在 8001 端口运行）

import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8001"
USERNAME = "tester01"
PASSWORD = "123456"


def call(method: str, path: str, body=None, token=None):
    """发请求，返回 (HTTP状态码, 响应JSON)"""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("token", token)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


passed = []


def check(label, condition, extra=""):
    mark = "✅" if condition else "❌"
    passed.append(condition)
    print(f"{mark} {label} {extra}")


# 1. 注册（重复注册要报 400）
code, res = call("POST", "/api/auth/register", {"username": USERNAME, "password": PASSWORD})
check("注册（或已存在）", res["code"] in ("200", "400"), f"code={res['code']} msg={res['msg']}")

code, res = call("POST", "/api/auth/register", {"username": USERNAME, "password": PASSWORD})
check("重复注册被拒", res["code"] == "400", f"msg={res['msg']}")

# 2. 登录拿 token
code, res = call("POST", "/api/auth/login", {"username": USERNAME, "password": PASSWORD})
check("登录成功", res["code"] == "200" and "token" in res["data"], f"msg={res['msg']}")
token = res["data"]["token"]
check("返回结构含 userInfo", "userInfo" in res["data"], f"data={res['data']}")

# 3. 密码错误
code, res = call("POST", "/api/auth/login", {"username": USERNAME, "password": "wrongpass"})
check("密码错误被拒", res["code"] == "400", f"msg={res['msg']}")

# 4. 未带 token → 应为 -1
code, res = call("GET", "/api/auth/me")
check("无 token 返回 -1", res["code"] == "-1", f"msg={res['msg']}")

# 5. 带 token 取当前用户
code, res = call("GET", "/api/auth/me", token=token)
check("带 token 取用户成功", res["code"] == "200", f"data={res['data']}")

# 6. 清空旧测试数据后建动作
code, res = call("GET", "/api/exercises", token=token)
for old in res["data"]:
    call("DELETE", f"/api/exercises/{old['id']}", token=token)

code, res = call("POST", "/api/exercises", {"name": "深蹲", "target_sets": 5}, token=token)
check("添加动作-深蹲", res["code"] == "200", f"data={res['data']}")
squat_id = res["data"]["id"]

code, res = call("POST", "/api/exercises", {"name": "卧推", "target_sets": 4}, token=token)
check("添加动作-卧推", res["code"] == "200", f"data={res['data']}")

code, res = call("POST", "/api/exercises", {"name": "深蹲", "target_sets": 5}, token=token)
check("同名动作被拒", res["code"] == "400", f"msg={res['msg']}")

# 7. 记录组数：第几组应自动递增
code, res = call("POST", f"/api/exercises/{squat_id}/sets", {"weight": 60, "reps": 10}, token=token)
check("记录第1组", res["data"]["set_number"] == 1, f"msg={res['msg']}")

code, res = call("POST", f"/api/exercises/{squat_id}/sets", {"weight": 60, "reps": 8}, token=token)
check("记录第2组（自动编号）", res["data"]["set_number"] == 2, f"msg={res['msg']}")

code, res = call("POST", f"/api/exercises/{squat_id}/sets", {"weight": 65, "reps": 6}, token=token)
check("记录第3组", res["data"]["set_number"] == 3, f"msg={res['msg']}")
first_set_id = None

# 8. 列表带今日组数
code, res = call("GET", "/api/exercises", token=token)
squat = [e for e in res["data"] if e["id"] == squat_id][0]
bench = [e for e in res["data"] if e["name"] == "卧推"][0]
check("深蹲今日 3 组", squat["today_sets"] == 3, f"today_sets={squat['today_sets']}")
check("卧推今日 0 组", bench["today_sets"] == 0, f"today_sets={bench['today_sets']}")

# 9. 组记录列表
code, res = call("GET", f"/api/exercises/{squat_id}/sets", token=token)
check("组记录列表 3 条", len(res["data"]) == 3, f"set_numbers={[s['set_number'] for s in res['data']]}")
first_set_id = res["data"][0]["id"]

# 10. 撤销一组
code, res = call("DELETE", f"/api/sets/{first_set_id}", token=token)
check("撤销一组成功", res["code"] == "200", f"msg={res['msg']}")

code, res = call("GET", f"/api/exercises/{squat_id}/sets", token=token)
check("撤销后剩 2 条", len(res["data"]) == 2, f"set_numbers={[s['set_number'] for s in res['data']]}")

# 11. 权限：别人的动作访问不到（用不存在的 id 测 404）
code, res = call("GET", "/api/exercises/999999/sets", token=token)
check("不存在动作返回 404", res["code"] == "404", f"msg={res['msg']}")

# 12. 参数校验：重量超范围 → 422
code, res = call("POST", f"/api/exercises/{squat_id}/sets", {"weight": 99999, "reps": 10}, token=token)
check("参数越界返回 422", res["code"] == "422", f"msg={res['msg']}")

# 13. 删动作（组记录应一起删）
code, res = call("DELETE", f"/api/exercises/{squat_id}", token=token)
check("删除动作成功", res["code"] == "200", f"msg={res['msg']}")

code, res = call("GET", f"/api/exercises/{squat_id}/sets", token=token)
check("动作删除后组记录也没了", res["code"] == "404", f"code={res['code']}")

print()
print(f"========== {sum(passed)}/{len(passed)} 项通过 ==========")
