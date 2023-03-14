from __future__ import absolute_import, unicode_literals

import datetime
import json
from random import randint

import requests
from celery import shared_task
from config.settings.components import config
from django_celery_beat.models import ClockedSchedule, PeriodicTask

URL_MAIN = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
URL_CHAT_ID = "?chat_id="
URL_TEXT = "&text="
TEXT_FOR_PATIENT = "Через час у вас встреча с психологом"
TEXT_FOR_PSYCHOLOGIST = "Через час у вас встреча с пациентом"

TASK_FOR_PATIENT = "send_notification_to_patient"
TASK_FOR_PSYCHOLOGIST = "send_notification_to_psychologist"


def make_notification_time(date_time, minutes_earlier=600000):
    """Создает время отправки оповещения"""
    return datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(
        minutes=minutes_earlier
    )


def make_notification_name(chat_id, date_time):
    """Создает имя оповещения"""
    return f"{chat_id}-{date_time}-{randint(0,10000)}"


def make_task(task, clocked_time, chat_id, date_time):
    """Создает задачу на отправку оповещения"""
    PeriodicTask.objects.create(
        clocked=clocked_time,
        name=make_notification_name(chat_id, date_time),
        task=task,
        args=json.dumps([chat_id]),
        one_off=True,
    )


def create_notification_tasks(psychologist_chat_id, patient_chat_id, date_time):
    """Создает задачи для оповещения пациента и психолога"""
    date_time = str(date_time)[:-6]
    clocked = ClockedSchedule.objects.create(clocked_time=make_notification_time(date_time))
    make_task(TASK_FOR_PSYCHOLOGIST, clocked, psychologist_chat_id, date_time)
    make_task(TASK_FOR_PATIENT, clocked, patient_chat_id, date_time)


@shared_task(name=TASK_FOR_PATIENT)
def send_notification_to_patient(chat_id):
    """Отправляет оповещение пациенту"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PATIENT)


@shared_task(name=TASK_FOR_PSYCHOLOGIST)
def send_notification_to_psychologist(chat_id):
    """Отправляет оповещение психологу"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PSYCHOLOGIST)
