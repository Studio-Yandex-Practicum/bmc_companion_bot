from django.contrib import admin

from . import models


@admin.register(models.TestCompleted)
class TestCompletedAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "test", "value")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "test", "question", "answer")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
