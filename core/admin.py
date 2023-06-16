from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "email",)
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ("user_permissions", "groups")
    list_filter = ("groups",)
