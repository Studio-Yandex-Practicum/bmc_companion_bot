from django.urls import path

from . import views

urlpatterns = [
    path("next_question", views.next_question),
    path("submit_answer", views.submit_answer),
    path("test_results", views.test_result),
    path("test_statuses/all", views.all_test_statuses),
]
