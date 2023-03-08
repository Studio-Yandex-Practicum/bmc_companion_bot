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


@admin.register(models.MeetingFeedback)
class MeetingFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "meeting", "score")
    list_select_related = ("meeting", "user")
    search_fields = (
        "user__first_name",
        "meeting__id",
    )
    list_filter = ("user", "meeting", "score")
