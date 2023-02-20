from content.models import Test
from questioning.models import TestCompleted, TestProgress
from rest_framework import serializers


class TestCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCompleted
        fields = ["id", "profile", "test", "value"]


class TestProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProgress
        fields = ["id", "profile", "question", "answer"]


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id"]
