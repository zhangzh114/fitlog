# fitness/backend/check_numbering.py
# 专项验证：删掉中间某一组后，再记录一组，组号不会和已有的撞车

import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8001"


def call(method, path, body=None, token=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("token", token)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))


token = call("POST", "/api/auth/login", {"username": "tester01", "password": "123456"})["data"]["token"]

ex = call("POST", "/api/exercises", {"name": "硬拉", "target_sets": 3}, token)["data"]
for i in range(3):
    call("POST", f"/api/exercises/{ex['id']}/sets", {"weight": 100 + i, "reps": 5}, token)

sets = call("GET", f"/api/exercises/{ex['id']}/sets", None, token)["data"]
print("初始组号:      ", [s["set_number"] for s in sets])

call("DELETE", f"/api/sets/{sets[0]['id']}", None, token)
sets = call("GET", f"/api/exercises/{ex['id']}/sets", None, token)["data"]
print("删掉第1组后:   ", [s["set_number"] for s in sets])

new = call("POST", f"/api/exercises/{ex['id']}/sets", {"weight": 110, "reps": 3}, token)["data"]
print("再记一组组号 =", new["set_number"], "（正确应为 4，若为 3 说明和已有组号撞车）")

call("DELETE", f"/api/exercises/{ex['id']}", None, token)
print("清理完成")
