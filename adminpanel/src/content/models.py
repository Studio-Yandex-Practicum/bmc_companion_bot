from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Test(models.Model):
    TEST_TYPE_UCE = 10
    TEST_TYPE_OTHER = 20

    TEST_TYPE_CHOICES = (
        (TEST_TYPE_UCE, "тест НДО"),
        (TEST_TYPE_OTHER, "прочее"),
    )

    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название")
    type = models.SmallIntegerField(
        null=True,
        blank=True,
        choices=TEST_TYPE_CHOICES,
        default=TEST_TYPE_OTHER,
        verbose_name="Тип теста",
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.type == self.TEST_TYPE_UCE:
            if Test.objects.filter(Q(type=self.TEST_TYPE_UCE) & ~Q(id=self.id)).exists():
                raise ValidationError("Тест НДО уже существует")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Question(models.Model):
    test = models.ForeignKey(
        Test, blank=False, null=True, on_delete=models.CASCADE, related_name="questions"
    )
    order_num = models.PositiveSmallIntegerField(
        blank=False, null=True, verbose_name="Порядковый номер"
    )
    text = models.TextField(blank=True, null=True, verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы тестов"

    def __str__(self):
        return f"{self.text[:30]}"

    def clean(self):
        if Question.objects.filter(
            Q(test=self.test) & Q(order_num=self.order_num) & ~Q(id=self.id)
        ).exists():
            raise ValidationError("Порядковый номер уже используется")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, blank=True, null=True, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=250, blank=True, null=True, verbose_name="Текст ответа")
    value = models.SmallIntegerField(
        null=True,
        blank=False,
        default=0,
        verbose_name="Баллы",
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"{self.text[:30]}"
