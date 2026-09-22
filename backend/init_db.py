# fitness/backend/init_db.py
# 【骨架·已给你写好】建表脚本
# 用法（在 fitness/backend 目录）：.\venv\Scripts\python.exe init_db.py

from app.database import Base, engine

import app.models  # noqa: F401  必须导入，让模型注册进 Base

Base.metadata.create_all(bind=engine)

print("建表完成！去 Navicat 刷新 fitness_dev 看看。")
