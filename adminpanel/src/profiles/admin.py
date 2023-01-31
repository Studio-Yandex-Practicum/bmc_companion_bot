from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(UserAdmin):
    list_display = ("id", "first_name", "last_name", "telegram_login", "phone")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telegram_login",
        "phone",
        "telegram_id",
        "chat_id",
    )
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (
            "Учетные данные",
            {"fields": ("username", "password", "email")},
        ),
        (
            "Основное",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "birthday",
                    "phone",
                    "age",
                    "uce_score",
                )
            },
        ),
        (
            "Telegram",
            {"fields": ("telegram_login", "telegram_id", "chat_id")},
        ),
        ("Персонал", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Полномочия", {"fields": ("groups", "user_permissions")}),
        (
            "Прочее",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
