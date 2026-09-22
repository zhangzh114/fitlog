# fitness/backend/app/response.py
# 【我写的】统一响应格式（信封）：{code, data, msg}
#
# 为什么要信封？
#   参考项目 ai_emotion 的前端拦截器就是按 data.code 来判断成功/失败的，
#   后端统一成这个格式，前端 request.js 就能通用；很多公司（尤其 Java 系）也这么约定。
# 代价：HTTP 状态码永远是 200，"成功/失败"放进 body 的 code 里（所以不如 REST 直观）。

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# HTTP 状态码 → 业务 code 的映射
# ⭐ '-1' 是"登录失效"的约定值：前端拦截器看到它就清 token 并跳登录页
CODE_MAP = {
    400: "400",
    401: "-1",
    403: "403",
    404: "404",
    422: "422",
    500: "500",
}


def success(data=None, msg="success"):
    """成功响应的信封"""
    return {"code": "200", "data": data, "msg": msg}


def register_exception_handlers(app: FastAPI):
    """把 FastAPI 抛的异常也包成信封（HTTP 一律 200，错误信息放 msg）"""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code = CODE_MAP.get(exc.status_code, str(exc.status_code))
        return JSONResponse(
            status_code=200,
            content={"code": code, "data": None, "msg": str(exc.detail)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        # 取第一条校验错误的信息，作为给用户的提示
        msg = errors[0].get("msg", "参数校验失败") if errors else "参数校验失败"
        return JSONResponse(
            status_code=200,
            content={"code": "422", "data": None, "msg": msg},
        )
