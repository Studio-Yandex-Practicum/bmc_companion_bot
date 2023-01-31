from rest_framework import serializers
from schedule.models import Meeting, Profile, TimeSlot


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("password",)


class TimeSlotSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = TimeSlot
        fields = "__all__"


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
