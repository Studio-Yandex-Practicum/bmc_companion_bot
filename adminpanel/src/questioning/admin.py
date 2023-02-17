from django.contrib import admin

from . import models


@admin.register(models.TestCompleted)
class TestCompletedAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "test", "value")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


"""без этой модели из админки не сбросить прохождение теста
@admin.register(models.TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "test",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
"""
