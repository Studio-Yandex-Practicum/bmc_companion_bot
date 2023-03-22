import datetime

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from schedule.api.v1 import serializer
from schedule.models import Meeting, MeetingFeedback, TimeSlot
from schedule.tasks import (
    create_feedback_notification,
    create_notification_tasks,
    delete_notification_tasks,
)


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = serializer.TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .order_by("date_start")
            .filter(date_start__gte=datetime.datetime.now())
        )
        is_free = self.request.query_params.get("is_free", None)
        if is_free == "True":
            qs = qs.filter(timeslot_meetings__isnull=True)
        return qs


class MeetingViewSet(ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = serializer.MeetingSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = [
        "id",
        "date_start",
        "format",
        "psychologist",
        "user",
    ]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = Meeting.objects.get(id=serializer.data.get("id"))
        task_data = serializer.validated_data
        create_notification_tasks(
            meeting_id=instance,
            psychologist_chat_id=task_data.get("psychologist").chat_id,
            patient_chat_id=task_data.get("user").chat_id,
            date_time=task_data.get("date_start"),
        )
        create_feedback_notification(
            meeting_id=instance,
            patient_chat_id=task_data.get("user").chat_id,
            date_time=task_data.get("date_start"),
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        delete_notification_tasks(
            meeting_id=instance,
            psychologist_chat_id=instance.psychologist.chat_id,
            patient_chat_id=instance.user.chat_id,
            date_time=instance.date_start,
        )
        task_data = serializer.validated_data
        create_notification_tasks(
            meeting_id=instance,
            psychologist_chat_id=task_data.get("psychologist").chat_id,
            patient_chat_id=task_data.get("user").chat_id,
            date_time=task_data.get("date_start"),
        )
        create_feedback_notification(
            meeting_id=instance,
            patient_chat_id=task_data.get("user").chat_id,
            date_time=task_data.get("date_start"),
        )
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        delete_notification_tasks(
            meeting_id=instance,
            psychologist_chat_id=instance.psychologist.chat_id,
            patient_chat_id=instance.user.chat_id,
            date_time=instance.timeslot.date_start,
        )
        return super().perform_destroy(instance)

    def get_queryset(self):
        qs = self.queryset
        is_active = self.request.query_params.get("is_active", None)
        user_id = self.request.query_params.get("user_id", None)
        past = self.request.query_params.get("past", None)
        if user_id:
            qs = qs.order_by("date_start").filter(user=user_id)
        if past == "True":
            qs = qs.filter(date_start__lte=datetime.datetime.now())
        if is_active == "True":
            qs = qs.filter(date_start__gte=datetime.datetime.now())
        return qs


class MeetingFeedbackViewSet(ModelViewSet):
    queryset = MeetingFeedback.objects.all()
    serializer_class = serializer.MeetingFeedbackSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = self.queryset
        is_active = self.request.query_params.get("is_active", None)
        meeting_id = self.request.query_params.get("meeting", None)
        user_id = self.request.query_params.get("user", None)
        if meeting_id and user_id:
            qs = super().get_queryset().filter(meeting=meeting_id, user=user_id)
        if is_active == "True":
            qs = qs.filter(date_start__gte=datetime.datetime.now())
        return qs
