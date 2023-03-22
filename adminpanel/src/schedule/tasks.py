from __future__ import absolute_import, unicode_literals

import datetime
import json
import time

import requests
from celery import shared_task
from config.settings.components import config
from django_celery_beat.models import ClockedSchedule
from loguru import logger
from profiles.models import Profile
from schedule.models import MeetingPeriodicTask

URL_MAIN = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
URL_CHAT_ID = "?chat_id="
URL_TEXT = "&text="

TEXT_FOR_PATIENT = "Напоминаем о встрече с психологом сегодня в"
TEXT_FOR_PSYCHOLOGIST = "Напоминаем о встрече с пациентом сегодня в"
TEXT_FOR_FEEDBACK = "Вы только что побывали на консультации. Пожалуйста, оставьте обратную связь."

TASK_FOR_PATIENT = "send_notification_to_patient"
TASK_FOR_PSYCHOLOGIST = "send_notification_to_psychologist"
TASK_FOR_FEEDBACK = "send_feedback_notification"
TASK_FOR_MAILING = "send_notification_to_everyone"


def make_notification_time(date_time, minutes=120, after=False):
    """Создает время отправки оповещения"""
    dt = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    if after:
        return dt + datetime.timedelta(minutes=minutes)
    return dt - datetime.timedelta(minutes=minutes)


def make_notification_name(task, chat_id, date_time):
    """Создает имя оповещения"""
    return f"{task}-{chat_id}-{date_time}"


def make_task(task, meeting_id, clocked_time, chat_id, date_time=" "):
    """Создает задачу на отправку оповещения"""
    MeetingPeriodicTask.objects.create(
        meeting=meeting_id,
        clocked=clocked_time,
        name=make_notification_name(task, chat_id, date_time),
        task=task,
        args=json.dumps([chat_id, date_time]),
        one_off=True,
    )


def delete_task(task, meeting):
    try:
        task = MeetingPeriodicTask.objects.get(meeting=meeting, task=task)

        task.delete()
    except Exception:
        return


def create_notification_tasks(meeting_id, psychologist_chat_id, patient_chat_id, date_time):
    """Создает задачи для оповещения пациента и психолога"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    clocked = ClockedSchedule.objects.create(clocked_time=make_notification_time(date_time))
    make_task(TASK_FOR_PSYCHOLOGIST, meeting_id, clocked, psychologist_chat_id, date_time)
    make_task(TASK_FOR_PATIENT, meeting_id, clocked, patient_chat_id, date_time)


def create_feedback_notification(meeting_id, patient_chat_id, date_time):
    """Создает задачу для напоминания о фидбеке"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    clocked = ClockedSchedule.objects.create(
        clocked_time=make_notification_time(date_time, minutes=70, after=True)
    )
    make_task(TASK_FOR_FEEDBACK, meeting_id, clocked, patient_chat_id, date_time)


def delete_notification_tasks(meeting_id, psychologist_chat_id, patient_chat_id, date_time):
    """Удаляет задачи для консультации"""
    date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    try:
        delete_task(TASK_FOR_PSYCHOLOGIST, meeting_id)
        delete_task(TASK_FOR_PATIENT, meeting_id)
        delete_task(TASK_FOR_FEEDBACK, meeting_id)
    except Exception as e:
        logger.error(
            "Error occurred in module %s while executing the function %s: %s"
            % (psychologist_chat_id, patient_chat_id, e)
        )
        return


@shared_task(name=TASK_FOR_PATIENT)
def send_notification_to_patient(chat_id, date_time):
    """Отправляет оповещение пациенту"""
    requests.get(
        URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PATIENT + date_time[10:]
    )


@shared_task(name=TASK_FOR_PSYCHOLOGIST)
def send_notification_to_psychologist(chat_id, date_time):
    """Отправляет оповещение психологу"""
    requests.get(
        URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_PSYCHOLOGIST + date_time[10:]
    )


@shared_task(name=TASK_FOR_FEEDBACK)
def send_feedback_notification(chat_id, date_time):
    """Отправляет оповещение после консультации"""
    requests.get(URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + TEXT_FOR_FEEDBACK)


@shared_task(name=TASK_FOR_MAILING)
def send_notification_to_everyone(text):
    chat_ids = Profile.objects.values_list("chat_id", flat=True)
    for chat_id in chat_ids:
        requests.get(
            URL_MAIN + URL_CHAT_ID + f"{chat_id}" + URL_TEXT + text + "&parse_mode=markdown"
        )
        time.sleep(1)
