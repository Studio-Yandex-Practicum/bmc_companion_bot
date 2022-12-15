import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


def get_db_url(config):
    db_url = config.DATABASE_URL
    if not db_url:
        db_url = "postgresql://{usr}:{pwd}@{host}:{port}/{db}".format(
            usr=config.POSTGRES_USER,
            pwd=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            db=config.POSTGRES_DB,
        )
    return db_url


class Settings(BaseSettings):
    SECRET_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DATABASE_URL: str = ""
    SQLALCHEMY_DATABASE_URI: str = ""
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    APP_HOST: str
    APP_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()
settings.SQLALCHEMY_DATABASE_URI = get_db_url(settings)
