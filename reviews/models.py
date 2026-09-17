from django.conf import settings
from django.db import models


class Review(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_reviews",
    )

    rating = models.PositiveIntegerField()

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "reviewer",
                    "business_user",
                ],
                name="unique_reviewer_business_review",
            )
        ]

    def __str__(self):
        return (
            f"{self.reviewer.username} -> "
            f"{self.business_user.username}"
        )