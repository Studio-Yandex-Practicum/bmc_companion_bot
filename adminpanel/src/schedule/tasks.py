from __future__ import absolute_import, unicode_literals

import datetime
import json

import requests
from celery import shared_task
from config.settings.components import config
from django_celery_beat.models import ClockedSchedule, PeriodicTask

BOT_TOKEN = config.BOT_TOKEN


def create_notification_task(chat_id, date_time):
    date_time = str(date_time)[:-6]
    clocked = ClockedSchedule.objects.create(
        clocked_time=datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        - datetime.timedelta(minutes=60)
    )
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f"{chat_id} {date_time}",
        task="send_notification",
        args=json.dumps([chat_id, date_time]),
        one_off=True,
    )


@shared_task(name="send_notification")
def send_notification(chat_id, datetime):
    task = PeriodicTask.objects.get(name=f"{chat_id} {datetime}")
    chat_id = task.name.split()[0]
    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}"
        f"&text=Через час у вас встреча с психологом"
    )
    requests.get(url)
