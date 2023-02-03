from content.models import Answer
from questioning.models import TestProgress


def get_test_result(user_id: int, test_id: int) -> int:
    answer_ids = TestProgress.objects.filter(profile_id=user_id, test_id=test_id).values_list(
        "answer_id", flat=True
    )
    answer_values = Answer.objects.filter(id__in=answer_ids).values_list("value", flat=True)
    return sum(answer_values)
