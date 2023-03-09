import datetime

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from schedule.api.v1 import serializer
from schedule.models import Meeting, MeetingFeedback, TimeSlot
from schedule.tasks import create_notification_tasks


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = serializer.TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset().filter(date_start__gte=datetime.datetime.now())
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
        task_data = serializer.validated_data
        create_notification_tasks(
            psychologist_chat_id=task_data.get("psychologist").chat_id,
            patient_chat_id=task_data.get("user").chat_id,
            date_time=task_data.get("date_start"),
        )
        return super().perform_create(serializer)

    def get_queryset(self):
        qs = self.queryset
        is_active = self.request.query_params.get("is_active", None)
        if is_active == "True":
            qs = super().get_queryset().filter(date_start__gte=datetime.datetime.now())
        return qs


class MeetingFeedbackViewSet(ModelViewSet):
    queryset = MeetingFeedback.objects.all()
    serializer_class = serializer.MeetingFeedbackSerializer
    permission_classes = [permissions.AllowAny]
