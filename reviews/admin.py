from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer",
        "business_user",
        "rating",
        "created_at",
        "updated_at",
    )
    list_filter = ("rating",)
    search_fields = (
        "reviewer__username",
        "business_user__username",
        "description",
    )