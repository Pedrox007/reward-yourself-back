from django.contrib import admin

from core.models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "email",)
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ("user_permissions", "groups")
    list_filter = ("groups",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "coin_reward", "expected_duration", "final_duration")
    search_fields = ("title", "description")
    ordering = ("user",)
    list_filter = ("user",)
