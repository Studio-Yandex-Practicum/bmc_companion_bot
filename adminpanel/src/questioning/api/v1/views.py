from http import HTTPStatus

from profiles.api.v1.serializer import ProfileSerializer
from profiles.models import Profile
from questioning.exceptions import AnswerNotFound, NoNextQuestion, QuestionNotActive
from questioning.services import (
    all_test_statuses,
    next_question,
    submit_answer,
    test_result,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
def profile_from_telegram(request: Request):
    telegram_id = request.data.get("telegram_id")
    if telegram_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data)


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_next_question(request: Request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    if any(id is None for id in [user_id, test_id]):
        return Response(status=HTTPStatus.BAD_REQUEST)
    try:
        next_question_data = next_question(user_id, test_id)
    except NoNextQuestion:
        return Response(status=HTTPStatus.NO_CONTENT)
    return Response(data=next_question_data, status=HTTPStatus.OK)


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def post_answer(request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    question_id = request.query_params.get("question_id")
    answer_id = request.query_params.get("answer_id")
    if any([id is None for id in [user_id, test_id, question_id, answer_id]]):
        return Response(status=HTTPStatus.BAD_REQUEST)
    try:
        confirmation_data = submit_answer(user_id, test_id, question_id, answer_id)
    except (QuestionNotActive, AnswerNotFound):
        return Response(status=HTTPStatus.BAD_REQUEST)
    return Response(data=confirmation_data, status=HTTPStatus.OK)


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_test_result(request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    if not all([id is not None for id in [user_id, test_id]]):
        return Response(status=HTTPStatus.BAD_REQUEST)
    result_data = test_result(user_id, test_id)
    return Response(data=result_data, status=HTTPStatus.OK)


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_all_test_statuses(request: Request):
    user_id = request.query_params.get("user_id")
    if user_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)
    status_data = all_test_statuses(user_id)
    return Response(data=status_data, status=HTTPStatus.OK)
