from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"timeslots", views.TimeSlotViewSet)
router.register(r"meetings", views.MeetingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
