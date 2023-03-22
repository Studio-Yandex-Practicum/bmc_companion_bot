from datetime import datetime

import openpyxl as openpyxl
from django.contrib import admin
from django.http import HttpResponse

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


@admin.action(description="Загрузить как файл *.xlsx")
def export_table_to_excel(modeladmin, request, queryset):
    data = (
        models.MeetingFeedback.objects.all()
        .order_by("meeting__timeslot__date_start")
        .values(
            "meeting__timeslot__date_start",
            "meeting__psychologist__last_name",
            "meeting__psychologist__first_name",
            "meeting__psychologist__telegram_login",
            "user__telegram_login",
            "text",
            "comfort_score",
            "better_score",
        )
    )
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(
        [
            "Дата",
            "Время",
            "Психолог",
            "Телеграм психолога",
            "Телеграм пациента",
            "Отзыв",
            "Оценка комфорта",
            "Оценка улучшений",
        ]
    )
    for row in reversed(data):
        ws.append(
            [
                row["meeting__timeslot__date_start"].strftime("%d.%m.%Y"),
                row["meeting__timeslot__date_start"].strftime("%H:%M"),
                row["meeting__psychologist__last_name"]
                + " "
                + row["meeting__psychologist__first_name"],
                row["meeting__psychologist__telegram_login"],
                row["user__telegram_login"],
                row["text"],
                row["comfort_score"],
                row["better_score"],
            ]
        )
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=feedbacks-{datetime.now()}.xlsx"
    wb.save(response)

    return response


@admin.register(models.MeetingFeedback)
class MeetingFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "meeting", "comfort_score", "better_score")
    list_select_related = ("meeting", "user")
    search_fields = (
        "user__first_name",
        "meeting__id",
    )
    list_filter = (
        "user",
        "meeting",
    )
    actions = [export_table_to_excel]
