from content.api.v1.serializer import QuestionSerializer, TestSerializer
from content.models import Answer, Question, Test
from django.db.models import Q
from profiles.models import Profile
from questioning.api.v1.serializers import TestProgressSerializer
from questioning.models import TestCompleted, TestProgress

from .exceptions import (
    AnswerNotFound,
    NoNextQuestion,
    QuestionNotActive,
    ResultNotFound,
)


def calculate_test_result(user_id: int, test_id: int) -> int:
    """Вычисление результата пройденного теста (суммирование стоимостей ответов)."""
    answer_ids = TestProgress.objects.filter(profile_id=user_id, test_id=test_id).values_list(
        "answer_id", flat=True
    )
    answer_values = Answer.objects.filter(id__in=answer_ids).values_list("value", flat=True)
    return sum(answer_values)


def finalize_test(user_id: int, test_id: int) -> None:
    """Создает запись о завершенном тесте. Обновляет профиль пользователя, если тип теста -- НДО."""
    value = calculate_test_result(user_id, test_id)
    TestCompleted.objects.create(profile_id=user_id, test_id=test_id, value=value)
    test = Test.objects.get(id=test_id)
    if test.type == test.TEST_TYPE_UCE:
        profile = Profile.objects.get(id=user_id)
        profile.uce_score = value
        profile.save()


def all_test_statuses(user_id: int) -> dict:
    """Получение статусов всех тестов для данного юзера."""
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
    data = {"user_id": user_id, "completed": completed, "active": active, "available": avalaible}
    return data


def next_question(user_id: int, test_id: int) -> dict:
    """Получение следующего вопроса для данного юзера в данном тесте."""
    if TestProgress.objects.filter(profile=user_id, test=test_id).first() is None:
        first_question = Question.objects.filter(test_id=test_id).order_by("order_num").first()
        test_progress = TestProgress.objects.create(
            profile_id=user_id, test_id=test_id, question_id=first_question.id
        )
    test_progress = (
        TestProgress.objects.filter(profile=user_id, test=test_id)
        .filter(answer__isnull=True)
        .first()
    )
    if test_progress is None:
        raise NoNextQuestion
    question = Question.objects.get(id=test_progress.question_id)
    serializer = QuestionSerializer(question)
    data = serializer.data
    data["user_id"] = user_id
    data["test_id"] = test_id
    return data


def submit_answer(user_id: int, test_id: int, question_id: int, answer_id: int) -> dict:
    """Получение следующего вопроса для данного юзера в данном тесте."""
    test_progress = (
        TestProgress.objects.filter(profile=user_id, test=test_id, question=question_id)
        .filter(answer__isnull=True)
        .first()
    )
    if test_progress is None:
        raise QuestionNotActive
    if not Answer.objects.filter(id=answer_id, question_id=question_id).exists():
        raise AnswerNotFound
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
        finalize_test(user_id, test_id)
    serializer = TestProgressSerializer(test_progress)
    data = {
        "user_id": serializer.data["profile"],
        "test_id": test_id,
        "test_question_id": serializer.data["question"],
        "answer_id": serializer.data["answer"],
    }
    return data


def test_result(user_id: int, test_id: int) -> dict[str, int]:
    """Получение информации о результате теста."""
    test_completed = TestCompleted.objects.filter(profile_id=user_id, test_id=test_id).first()
    if test_completed is None:
        raise ResultNotFound
    test = Test.objects.get(id=test_id)
    value = test_completed.value
    data = {"user_id": user_id, "id": test.id, "type": test.type, "name": test.name, "value": value}
    return data
