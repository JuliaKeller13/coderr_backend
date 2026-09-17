from django.conf import settings
from django.db import models


class Profile(models.Model):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    type = models.CharField(
        max_length=10,
        choices=UserType.choices,
    )
    
    file = models.FileField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    tel = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    working_hours = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
