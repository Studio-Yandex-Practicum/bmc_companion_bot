import os
from pathlib import Path

from celery import Celery
from config.settings.components import config

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

BOT_TOKEN = config.BOT_TOKEN

app = Celery("config.celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
