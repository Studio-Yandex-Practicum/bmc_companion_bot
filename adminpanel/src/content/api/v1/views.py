from content.api.v1 import serializer
from content.models import Answer, Question, Test
from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = serializer.TestSerializer
    http_method_names = ["get"]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        prefetch_answers = Prefetch("answers", Answer.objects.all())
        prefetch_questions = Prefetch(
            "questions", Question.objects.all().prefetch_related(prefetch_answers)
        )
        qs = qs.prefetch_related(prefetch_questions)
        return qs
