# fitness/backend/app/routers/exercises.py
# 【我写的】训练相关接口：动作的增删查 + 组记录的增删查
#
# 核心业务：POST /api/exercises/{id}/sets 会自动算出"第几组"

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user, get_db
from app.response import success

router = APIRouter(prefix="/api", tags=["训练"])


def _today_start() -> datetime:
    """今天的 0 点，用来统计'今日组数'"""
    return datetime.combine(date.today(), datetime.min.time())


def _get_my_exercise(exercise_id: int, db: Session, current_user: models.User) -> models.Exercise:
    """取动作，并检查是不是当前用户的（安全底线：不能碰别人的数据）"""
    exercise = db.get(models.Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="动作不存在")
    if exercise.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能操作自己的动作")
    return exercise


# ---------------- 动作 ----------------


@router.get("/exercises")
def list_exercises(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """我的动作列表，每个动作带上'今日已完成组数'"""
    exercises = db.scalars(
        select(models.Exercise)
        .where(models.Exercise.user_id == current_user.id)
        .order_by(models.Exercise.id)
    ).all()

    # 一次查出所有动作的今日组数（GROUP BY），避免循环里反复查数据库
    rows = db.execute(
        select(models.SetLog.exercise_id, func.count())
        .where(
            models.SetLog.user_id == current_user.id,
            models.SetLog.created_at >= _today_start(),
        )
        .group_by(models.SetLog.exercise_id)
    ).all()
    today_map = {exercise_id: count for exercise_id, count in rows}

    data = [
        schemas.ExerciseOut(
            id=ex.id,
            name=ex.name,
            target_sets=ex.target_sets,
            today_sets=today_map.get(ex.id, 0),
        ).model_dump()
        for ex in exercises
    ]
    return success(data)


@router.post("/exercises")
def create_exercise(
    data: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """添加动作（同一个用户下不允许重名）"""
    exists = db.scalar(
        select(models.Exercise).where(
            models.Exercise.user_id == current_user.id,
            models.Exercise.name == data.name,
        )
    )
    if exists:
        raise HTTPException(status_code=400, detail="这个动作已经有了")

    exercise = models.Exercise(
        name=data.name, target_sets=data.target_sets, user_id=current_user.id
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return success(
        schemas.ExerciseOut(
            id=exercise.id, name=exercise.name, target_sets=exercise.target_sets, today_sets=0
        ).model_dump(),
        msg="添加成功",
    )


@router.delete("/exercises/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """删除动作（它的组记录会被 cascade 一起删掉）"""
    exercise = _get_my_exercise(exercise_id, db, current_user)
    db.delete(exercise)
    db.commit()
    return success(msg="删除成功")


# ---------------- 组记录 ----------------


@router.get("/exercises/{exercise_id}/sets")
def list_sets(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """某个动作的所有组记录（按第几组排序）"""
    _get_my_exercise(exercise_id, db, current_user)
    sets = db.scalars(
        select(models.SetLog)
        .where(models.SetLog.exercise_id == exercise_id)
        .order_by(models.SetLog.set_number)
    ).all()
    return success([schemas.SetOut.model_validate(s).model_dump() for s in sets])


@router.post("/exercises/{exercise_id}/sets")
def add_set(
    exercise_id: int,
    data: schemas.SetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """⭐ 记录一组：第几组 = 该动作已有组数 + 1（由后端算，不信前端）"""
    _get_my_exercise(exercise_id, db, current_user)

    # 取该动作当前"最大组号" + 1
    # 用 max 而不是 count：删掉中间某一组后，再记录也不会和已有组号撞车
    max_number = db.scalar(
        select(func.max(models.SetLog.set_number)).where(
            models.SetLog.exercise_id == exercise_id
        )
    )

    new_set = models.SetLog(
        user_id=current_user.id,
        exercise_id=exercise_id,
        set_number=(max_number or 0) + 1,
        weight=data.weight,
        reps=data.reps,
    )
    db.add(new_set)
    db.commit()
    db.refresh(new_set)
    return success(schemas.SetOut.model_validate(new_set).model_dump(), msg=f"第 {new_set.set_number} 组已记录")


@router.delete("/sets/{set_id}")
def delete_set(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """撤销一组（记错了可以删）"""
    one_set = db.get(models.SetLog, set_id)
    if one_set is None:
        raise HTTPException(status_code=404, detail="记录不存在")
    if one_set.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能删除自己的记录")

    db.delete(one_set)
    db.commit()
    return success(msg="已撤销")
