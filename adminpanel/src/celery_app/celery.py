import os
from pathlib import Path

import requests
from celery import Celery, shared_task
from django_celery_beat.models import PeriodicTask
from pydantic import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@shared_task(name="send_notification")
def send_notification(chat_id, datetime):
    task = PeriodicTask.objects.get(name=f"{chat_id} {datetime}")
    chat_id, datetime = task.split()
    url = (
        f"https://api.telegram.org/"
        f"bot{settings.BOT_TOKEN}/sendMessage?chat_id={chat_id}"
        "&text=meeting in one hour"
    )
    requests.get(url)
