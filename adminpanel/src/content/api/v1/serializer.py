from content.models import Answer, Question, Test, TestCompleted, TestProgress
from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "value"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ["id", "name", "type", "questions"]


class TestCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCompleted
        fields = ["id", "profile", "test", "value"]


class TestProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProgress
        fields = ["id", "profile", "question", "answer"]
