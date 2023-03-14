from __future__ import absolute_import, unicode_literals

import datetime
import json

import requests
from celery import shared_task
from config.settings.components import config
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from loguru import logger

URL_MAIN = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
URL_CHAT_ID = "?chat_id="
URL_TEXT = "&text="

TEXT_FOR_PATIENT = "Через час у вас встреча с психологом"
TEXT_FOR_PSYCHOLOGIST = "Через час у вас встреча с пациентом"
TEXT_FOR_FEEDBACK = "Вы только что побывали на консультации. Пожалуйста, оставьте обратную связь."

TASK_FOR_PATIENT = "send_notification_to_patient"
TASK_FOR_PSYCHOLOGIST = "send_notification_to_psychologist"
TASK_FOR_FEEDBACK = "send_feedback_notification"


def make_notification_time(date_time, minutes_earlier=1000000):
    """Создает время отправки оповещения"""
    return datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M") - datetime.timedelta(
        minutes=minutes_earlier
    )


def make_notification_name(task, chat_id, date_time):
    """Создает имя оповещения"""
    return f"{task}-{chat_id}-{date_time}"


def make_task(task, clocked_time, chat_id, date_time):
    """Создает задачу на отправку оповещения"""
    PeriodicTask.objects.create(
        clocked=clocked_time,
        name=make_notification_name(task, chat_id, date_time),
        task=task,
        args=json.dumps([chat_id]),
        one_off=True,
    )


def delete_task(task, chat_id, date_time):
    try:

        name = make_notification_name(task, chat_id, date_time)
        task = PeriodicTask.objects.get(name=name, task=task)

        task.delete()
    except Exception as e:
        logger.error(
            "Error occurred in module %s while executing the function %s: %s" % (chat_id, task, e)
        )
        return


def create_notification_tasks(psychologist_chat_id, patient_chat_id, date_time):
    """Создает задачи для оповещения пациента и психолога"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    clocked = ClockedSchedule.objects.create(clocked_time=make_notification_time(date_time))
    make_task(TASK_FOR_PSYCHOLOGIST, clocked, psychologist_chat_id, date_time)
    make_task(TASK_FOR_PATIENT, clocked, patient_chat_id, date_time)


def create_feedback_notification(patient_chat_id, date_time):
    """Создает задачу для напоминания о фидбеке"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    clocked = ClockedSchedule.objects.create(clocked_time=make_notification_time(date_time))
    make_task(TASK_FOR_FEEDBACK, clocked, patient_chat_id, date_time)


def delete_notification_tasks(psychologist_chat_id, patient_chat_id, date_time):
    """Удаляет задачи для консультации"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    try:
        delete_task(TASK_FOR_PSYCHOLOGIST, psychologist_chat_id, date_time)
        delete_task(TASK_FOR_PATIENT, patient_chat_id, date_time)
        delete_task(TASK_FOR_FEEDBACK, patient_chat_id, date_time)
    except Exception as e:
        logger.error(
            "Error occurred in module %s while executing the function %s: %s"
            % (psychologist_chat_id, patient_chat_id, e)
        )
        return


@shared_task(name=TASK_FOR_PATIENT)
def send_notification_to_patient(chat_id):
    """Отправляет оповещение пациенту"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PATIENT)


@shared_task(name=TASK_FOR_PSYCHOLOGIST)
def send_notification_to_psychologist(chat_id):
    """Отправляет оповещение психологу"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PSYCHOLOGIST)


@shared_task(name=TASK_FOR_FEEDBACK)
def send_feedback_notification(chat_id):
    """Отправляет оповещение после консультации"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_FEEDBACK)
