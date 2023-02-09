from django.urls import path

from . import views

urlpatterns = [
    path("next_question", views.get_next_question),
    path("submit_answer", views.post_answer),
    path("test_results", views.get_test_result),
    path("test_statuses/all", views.get_all_test_statuses),
]
