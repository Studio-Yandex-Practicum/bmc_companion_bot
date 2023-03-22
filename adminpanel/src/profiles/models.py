from django.contrib.auth.models import AbstractUser
from django.db import models
from django_celery_beat.models import PeriodicTask


class Profile(AbstractUser):
    middle_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Отчество")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name="Телефон")
    telegram_login = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Telegram login"
    )
    age = models.SmallIntegerField(null=True, blank=True, verbose_name="Возраст")
    uce_score = models.SmallIntegerField(
        null=True, blank=True, default=0, verbose_name="Балл за тест НДО"
    )
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram id")
    chat_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram chat_id")

    def __str__(self):
        return f"{self.first_name} ({self.telegram_login})"


class AllUsersNotification(PeriodicTask):
    text = models.TextField()
