import datetime

from celery_app.create_task import create_notification_task
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from schedule.api.v1 import serializer
from schedule.models import Meeting, TimeSlot


class TimeSlotViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = serializer.TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset().filter(date_start__gte=datetime.datetime.now())
        return qs


class MeetingViewSet(ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = serializer.MeetingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        create_notification_task(chat_id=serializer.validated_data.get("user").chat_id)
        return super().perform_create(serializer)
