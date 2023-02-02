import json
from datetime import datetime as dt

from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def create_notification_task(chat_id, date_time=str(dt.now())):
    PeriodicTask.objects.create(
        name=f"{chat_id}",
        task="send_notification",
        interval=IntervalSchedule.objects.get_or_create(every=10, period="seconds")[0],
        args=json.dumps([chat_id, date_time]),
        start_time=timezone.now(),
    )
