from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"profiles", views.ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
