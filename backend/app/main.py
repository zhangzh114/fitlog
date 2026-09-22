# fitness/backend/app/main.py
# 【我写的】应用入口：注册异常处理（信封格式）、挂载路由、CORS

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.response import register_exception_handlers
from app.routers import auth, exercises

app = FastAPI(title="Fitlog健身日志 API")

# 统一响应格式：所有异常也返回 {code, data, msg}
register_exception_handlers(app)

# CORS：uni-app 的 H5 版 / 直接访问接口时需要
# （Web 版走 Vite 代理，本来就不跨域；这里配着更保险）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(exercises.router)


@app.get("/")
def root():
    return {"message": "Fitlog健身日志后端启动成功!"}
