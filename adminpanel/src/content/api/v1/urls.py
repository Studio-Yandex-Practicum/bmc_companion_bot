from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"tests", views.TestViewSet)

urlpatterns = [
    path("next_question", views.next_question),
    path("submit_answer", views.submit_answer),
    path("test_statuses/all", views.all_test_statuses),
    path("", include(router.urls)),
]
