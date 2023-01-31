from django.urls import include, path

urlpatterns = [
    path("v1/", include("content.api.v1.urls")),
]
