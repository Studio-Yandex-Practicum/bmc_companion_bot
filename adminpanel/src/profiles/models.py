from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    middle_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Отчество")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон")
    telegram_login = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="TG login"
    )
    age = models.SmallIntegerField(null=True, blank=True, verbose_name="Возраст")
    uce_score = models.SmallIntegerField(
        null=True, blank=True, default=0, verbose_name="Бал за тест НДО"
    )
    telegram_id = models.CharField(max_length=200, null=True, blank=True, verbose_name="TG id")
    chat_id = models.CharField(max_length=200, null=True, blank=True, verbose_name="TG chat_id")

    def __str__(self):
        return f"{self.first_name} ({self.telegram_login})"
