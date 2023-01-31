from django.contrib import admin

from . import models


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "date_start")
    list_select_related = ("profile",)
    search_fields = (
        "profile__first_name",
        "profile__last_name",
        "profile__telegram_login",
        "profile__phone",
        "profile__telegram_id",
        "profile__chat_id",
    )


@admin.register(models.Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "psychologist", "user", "date_start", "format")
    list_select_related = ("psychologist", "user")
    search_fields = (
        "psychologist__first_name",
        "psychologist__phone",
        "psychologist__telegram_login",
        "user__first_name",
        "user__phone",
        "user__telegram_login",
    )
    list_filter = ("psychologist", "format")
