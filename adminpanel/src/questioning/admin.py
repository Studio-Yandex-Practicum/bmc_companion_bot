from django.contrib import admin

from . import models


@admin.register(models.TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "test", "question", "answer")
