from django.urls import include, path

urlpatterns = [
    path("v1/", include("questioning.api.v1.urls")),
]
