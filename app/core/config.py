import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Appointment App Backend"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
