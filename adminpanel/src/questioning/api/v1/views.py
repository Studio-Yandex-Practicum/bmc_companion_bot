from http import HTTPStatus

from content.api.v1.serializer import QuestionSerializer, TestSerializer
from content.models import Question, Test
from django.db.models import Q
from profiles.api.v1.serializer import ProfileSerializer
from profiles.models import Profile
from questioning.api.v1.serializers import TestProgressSerializer
from questioning.models import TestCompleted, TestProgress
from questioning.services import get_test_result
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def next_question(request: Request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    if user_id is None or test_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)

    if TestProgress.objects.filter(profile=user_id, test=test_id).first() is None:
        first_question = Question.objects.filter(test_id=test_id).order_by("order_num").first()
        test_progress = TestProgress.objects.create(
            profile_id=user_id, test_id=test_id, question_id=first_question.id
        )
        print("created", test_progress)
    test_progress = (
        TestProgress.objects.filter(profile=user_id, test=test_id)
        .filter(answer__isnull=True)
        .first()
    )
    if test_progress is None:
        return Response(status=HTTPStatus.NO_CONTENT)
    question = Question.objects.get(id=test_progress.question_id)
    serializer = QuestionSerializer(question)
    data = serializer.data
    data["user_id"] = user_id
    data["test_id"] = test_id
    print("data_sent_as_next_Question:", data)
    return Response(data=data, status=HTTPStatus.OK)


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def submit_answer(request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    question_id = request.query_params.get("question_id")
    answer_id = request.query_params.get("answer_id")
    if not all([id is not None for id in [user_id, test_id, question_id, answer_id]]):
        return Response(status=HTTPStatus.BAD_REQUEST)
    test_progress = (
        TestProgress.objects.filter(profile=user_id, test=test_id, question=question_id)
        .filter(answer__isnull=True)
        .first()
    )
    if test_progress is None:
        return Response(status=HTTPStatus.BAD_REQUEST)
    test_progress.answer_id = answer_id
    test_progress.save()
    current_order_num = Question.objects.get(id=question_id).order_num
    next_question = (
        Question.objects.filter(test=test_id)
        .filter(order_num__gt=current_order_num)
        .order_by("order_num")
        .first()
    )
    if next_question is not None:
        TestProgress.objects.create(
            profile_id=user_id, test_id=test_id, question_id=next_question.id
        )
    else:
        value = get_test_result(user_id, test_id)
        TestCompleted.objects.create(profile_id=user_id, test_id=test_id, value=value)
    serializer = TestProgressSerializer(test_progress)
    data = {}
    data["user_id"] = serializer.data["profile"]
    data["test_id"] = test_id
    data["test_question_id"] = serializer.data["question"]
    data["answer_id"] = serializer.data["answer"]
    return Response(data=data)


@api_view(["GET"])
def profile_from_telegram(request: Request):
    telegram_id = request.data["telegram_id"]
    profile = Profile.objects.filter(telegram_id=telegram_id).first()
    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data)


@api_view(["GET"])
def all_test_results(request):
    pass


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def test_result(request):
    user_id = request.query_params.get("user_id")
    test_id = request.query_params.get("test_id")
    if not all([id is not None for id in [user_id, test_id]]):
        return Response(status=HTTPStatus.BAD_REQUEST)
    test_completed = TestCompleted.objects.filter(profile_id=user_id, test_id=test_id).first()
    if test_completed is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    test = Test.objects.get(id=test_id)
    value = test_completed.value
    # TODO: запись результата НДО в профиль юзера
    data = {"user_id": user_id, "id": test.id, "type": test.type, "name": test.name, "value": value}
    return Response(data=data, status=HTTPStatus.OK)


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
    user_id = request.query_params.get("user_id")
    if user_id is None:
        return Response(status=HTTPStatus.BAD_REQUEST)
    completed_test_id = TestCompleted.objects.values_list("test_id", flat=True)
    active_question_id = TestProgress.objects.filter(answer_id__isnull=True).values_list(
        "question_id", flat=True
    )
    active_test_id = Question.objects.filter(Q(id__in=active_question_id)).values_list(
        "test_id", flat=True
    )
    completed_tests = Test.objects.filter(Q(id__in=completed_test_id)).all()
    active_tests = Test.objects.filter(Q(id__in=active_test_id)).all()
    avalaible_tests = (
        Test.objects.filter(~Q(id__in=completed_test_id)).filter(~Q(id__in=active_test_id)).all()
    )
    completed = TestSerializer(completed_tests, many=True).data
    active = TestSerializer(active_tests, many=True).data
    avalaible = TestSerializer(avalaible_tests, many=True).data
    return Response(
        data={"user_id": user_id, "completed": completed, "active": active, "available": avalaible},
        status=HTTPStatus.OK,
    )


@api_view(["GET"])
def check_answer(request):
    pass
