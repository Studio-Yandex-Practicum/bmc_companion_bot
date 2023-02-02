from content.api.v1 import serializer
from content.models import Answer, Profile, Question, Test, TestProgress
from django.db.models import Prefetch
from profiles.api.v1.serializer import ProfileSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializer import QuestionSerializer, TestProgressSerializer


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


@api_view(["GET"])
def next_question(request: Request):
    question = Question.objects.first()  # TODO: логика выбора вопроса
    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(["POST"])
def submit_answer(request):
    progress = TestProgress.objects.first()  # TODO: логика записи прогресса
    serializer = TestProgressSerializer(progress)
    return Response(serializer.data)


@api_view(["GET"])
def profile_from_telegram(request: Request):
    telegram_id = request.data["telegram_id"]
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(["GET"])
def all_test_results(request):
    pass


@api_view(["GET"])
def test_result(request):
    pass


@api_view(["GET"])
def test_status(request):
    pass


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def all_test_statuses(request: Request):
    user_id = request.query_params.get("user_id")  # TODO: логика списков тестов
    return Response(
        data={"user_id": user_id, "completed": [], "active": [], "available": []}, status=200
    )


@api_view(["GET"])
def check_answer(request):
    pass
