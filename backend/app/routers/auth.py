# fitness/backend/app/routers/auth.py
# 【我写的】注册 / 登录 / 我是谁
# 统一用信封格式返回：success(data)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import create_access_token, get_current_user, get_db, hash_password, verify_password
from app.response import success

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(data: schemas.UserRegister, db: Session = Depends(get_db)):
    """注册"""
    exists = db.scalar(select(models.User).where(models.User.username == data.username))
    if exists:
        raise HTTPException(status_code=400, detail="用户名已被注册")

    user = models.User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return success(schemas.UserOut.model_validate(user).model_dump(), msg="注册成功")


@router.post("/login")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """登录：返回 token + userInfo（和参考项目的结构保持一致）"""
    user = db.scalar(select(models.User).where(models.User.username == data.username))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    return success(
        {
            "token": create_access_token(user.id),
            "userInfo": {"id": user.id, "username": user.username},
        },
        msg="登录成功",
    )


@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    """当前登录用户（前端刷新页面后用它恢复登录态）"""
    return success({"id": current_user.id, "username": current_user.username})
