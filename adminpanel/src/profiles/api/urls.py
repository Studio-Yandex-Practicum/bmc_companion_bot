from django.urls import include, path

urlpatterns = [
    path("v1/", include("profiles.api.v1.urls")),
]
