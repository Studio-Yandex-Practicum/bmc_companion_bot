from django.contrib import admin

from . import models


class InlineQuestionAdmin(admin.TabularInline):
    model = models.Question
    fields = ("text",)
    extra = 0


class InlineAnswerAdmin(admin.TabularInline):
    model = models.Answer
    fields = ("text", "value")
    extra = 0


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name",)
    list_filter = ("type",)
    inlines = (InlineQuestionAdmin,)


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "text")
    list_select_related = ("test",)
    search_fields = ("test__name", "text")
    list_filter = ("test",)
    inlines = (InlineAnswerAdmin,)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "text", "value")
    list_select_related = ("question__test", "question")
    search_fields = ("question__test__name", "question__text", "text")
    list_filter = ("question__test", "question", "value")
