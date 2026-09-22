# fitness/backend/app/models.py
# 【我写的】表结构"图纸"：一个类 = 一张表

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """用户表 users"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="user")


class Exercise(Base):
    """动作表 exercises：深蹲、卧推……一个人可以有多个动作"""
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_sets: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    user: Mapped["User"] = relationship(back_populates="exercises")
    # cascade：删动作时，它的组记录一起删掉（避免留下孤儿数据）
    set_logs: Mapped[list["SetLog"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )


class SetLog(Base):
    """组记录表 set_logs：每一组做了多重(kg)、多少次"""
    __tablename__ = "set_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    # ⭐ 第几组：由后端算出来（该动作已有组数 + 1），不由前端传
    set_number: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 重量 kg
    reps: Mapped[int] = mapped_column(Integer, default=0, nullable=False)    # 次数
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    exercise: Mapped["Exercise"] = relationship(back_populates="set_logs")
