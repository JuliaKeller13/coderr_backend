from django.contrib import admin

from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "type",
        "location",
        "created_at",
    )
    list_filter = ("type",)
    search_fields = (
        "user__username",
        "user__email",
        "location",
    )
