from content.models import Answer, Question, Test
from django.db import models
from profiles.models import Profile


class TestProgress(models.Model):
    profile = models.ForeignKey(
        Profile, blank=False, null=True, on_delete=models.CASCADE, related_name="answered"
    )
    test = models.ForeignKey(
        Test, blank=False, null=True, on_delete=models.CASCADE, related_name="answered"
    )
    question = models.ForeignKey(
        Question, blank=False, null=True, on_delete=models.CASCADE, related_name="answered"
    )
    answer = models.ForeignKey(
        Answer, blank=True, null=True, on_delete=models.CASCADE, related_name="used_in"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ответ на вопрос теста"
        verbose_name_plural = "Ответы на вопрос теста"


class TestCompleted(models.Model):
    profile = models.ForeignKey(
        Profile, blank=False, null=True, on_delete=models.CASCADE, related_name="test_results"
    )
    test = models.ForeignKey(
        Test, blank=False, null=True, on_delete=models.CASCADE, related_name="results"
    )
    value = models.SmallIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name="Результат теста (баллы)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
