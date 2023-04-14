from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"timeslots", views.TimeSlotViewSet)
router.register(r"meetings", views.MeetingViewSet)
router.register(r"meeting_feedbacks", views.MeetingFeedbackViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
