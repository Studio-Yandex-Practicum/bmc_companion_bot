from profiles.api.v1 import serializer
from profiles.models import Profile
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializer.ProfileSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "middle_name",
        "phone",
        "telegram_id",
        "chat_id",
        "telegram_login",
        "address",
    ]

    def get_queryset(self):
        qs = self.queryset
        if _id := self.request.query_params.get("id", None):
            qs = qs.filter(id=_id)
        return qs
