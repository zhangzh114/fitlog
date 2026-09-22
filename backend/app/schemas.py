# fitness/backend/app/schemas.py
# 【我写的】接口的输入/输出格式（Pydantic）
#
# 注意：用了 {code,data,msg} 信封后，路由不再写 response_model=xxx，
# 所以下面的 Out 系列主要用来"把 ORM 对象转成 dict"，让 data 里的字段干净可控。

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- 认证 ----------

class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=64)


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- 动作 ----------

class ExerciseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    target_sets: int = Field(default=4, ge=1, le=20)


class ExerciseOut(BaseModel):
    id: int
    name: str
    target_sets: int
    today_sets: int = 0  # 今日已完成组数（接口里临时算出来的）

    model_config = ConfigDict(from_attributes=True)


# ---------- 组记录 ----------

class SetCreate(BaseModel):
    weight: int = Field(default=0, ge=0, le=1000)
    reps: int = Field(default=0, ge=0, le=1000)


class SetOut(BaseModel):
    id: int
    exercise_id: int
    set_number: int
    weight: int
    reps: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
