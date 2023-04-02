from pathlib import Path
from urllib.parse import urljoin

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMINPANEL_HOST: str
    ADMINPANEL_PORT: str
    ADMINPANEL_WEB_PROTOCOL: str

    class Config:
        env_file = ROOT_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()

API_PATH_PREFIX = "api/"
API_V1_PATH_PREFIX = "v1/"

BASE_URL = (
    f"{settings.ADMINPANEL_WEB_PROTOCOL}://{settings.ADMINPANEL_HOST}:"
    f"{settings.ADMINPANEL_PORT}/"
)
BASE_API_URL = urljoin(BASE_URL, API_PATH_PREFIX)
BASE_API_URL_V1 = urljoin(BASE_API_URL, API_V1_PATH_PREFIX)

WEB_API_URL = f"{settings.ADMINPANEL_HOST}:{settings.ADMINPANEL_PORT}"
