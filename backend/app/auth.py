# fitness/backend/app/auth.py
# 【我写的】密码哈希 + JWT + 当前用户依赖 + 数据库会话依赖
# 注意：按参考项目的约定，令牌放在请求头 `token` 里（不是 Authorization: Bearer）

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import SessionLocal

ALGORITHM = "HS256"

# 从请求头 token 里取令牌（auto_error=False 表示没有也不报错，我们自己控制提示）
token_header = APIKeyHeader(name="token", auto_error=False)


def get_db():
    """每个请求自动开一个数据库会话，用完关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    """注册时：明文密码 → 不可逆哈希"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """登录时：比对输入密码与库里的哈希"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    """签发 JWT：把用户 id 装进去，7 天过期"""
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def get_current_user(
    token: str | None = Security(token_header),
    db: Session = Depends(get_db),
) -> models.User:
    """守门员：解析令牌 → 找到用户 → 交给接口函数"""
    unauthorized = HTTPException(status_code=401, detail="登录已过期，请重新登录")

    if not token:
        raise unauthorized

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise unauthorized  # 伪造/过期/格式错

    user = db.scalar(select(models.User).where(models.User.id == user_id))
    if user is None:
        raise unauthorized
    return user
