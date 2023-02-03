import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str
    ALLOWED_HOSTS: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    BOT_TOKEN: str
    DJANGO_SETTINGS_MODULE: str

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


config = Settings()
