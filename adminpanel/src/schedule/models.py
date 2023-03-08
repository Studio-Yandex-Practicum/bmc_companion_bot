from django.db import models
from profiles.models import Profile


class TimeSlot(models.Model):
    profile = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.CASCADE, related_name="timeslots"
    )
    date_start = models.DateTimeField(null=True, blank=True, verbose_name="Дата старта")

    class Meta:
        verbose_name = "Таймслот"
        verbose_name_plural = "Таймслоты"


class Meeting(models.Model):
    MEETING_FORMAT_ONLINE = 10
    MEETING_FORMAT_OFFLINE = 20

    MEETING_FORMAT_CHOICES = (
        (MEETING_FORMAT_ONLINE, "онлайн"),
        (MEETING_FORMAT_OFFLINE, "очно"),
    )

    psychologist = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="meetings",
        verbose_name="Психолог",
    )
    user = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_meetings",
        verbose_name="Пациент",
    )
    comment = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Запрос к психологу"
    )
    date_start = models.DateTimeField(null=True, blank=True, verbose_name="Дата старта")
    format = models.SmallIntegerField(
        null=True,
        blank=True,
        choices=MEETING_FORMAT_CHOICES,
        default=MEETING_FORMAT_ONLINE,
        verbose_name="Формат встречи",
    )
    timeslot = models.OneToOneField(
        TimeSlot,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="timeslot_meetings",
        verbose_name="Таймслот",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"
        ordering = ["id"]


class MeetingFeedback(models.Model):
    user = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feedbacks",
        verbose_name="Пациент",
    )
    meeting = models.ForeignKey(
        Meeting,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name="Консультация",
    )
    text = models.TextField(null=True, blank=True, verbose_name="Текст отзыва")
    score = models.SmallIntegerField(null=True, blank=True, verbose_name="Оценка")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
