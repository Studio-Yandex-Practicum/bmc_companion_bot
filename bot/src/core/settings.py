import os
from pathlib import Path
from urllib.parse import urljoin

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str
    APP_HOST: str
    APP_PORT: str
    APP_WEB_PROTOCOL: str
    ADMIN: str
    ROOT: str
    USER: str

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()

API_PATH_PREFIX = "api/"
API_V1_PATH_PREFIX = "v1/"

BASE_URL = f"{settings.APP_WEB_PROTOCOL}://{settings.APP_HOST}:{settings.APP_PORT}/"
BASE_API_URL = urljoin(BASE_URL, API_PATH_PREFIX)
BASE_API_URL_V1 = urljoin(BASE_API_URL, API_V1_PATH_PREFIX)
