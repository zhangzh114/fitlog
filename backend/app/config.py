# fitness/backend/app/config.py
# 【骨架·已给你写好，直接复用博客项目的做法】

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root:123456@127.0.0.1:3306/fitness_dev?charset=utf8mb4"
    jwt_secret: str = "fitness-dev-secret"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
