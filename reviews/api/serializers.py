from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reviews.models import Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        reviewer = self.context["request"].user

        return Review.objects.create(
            reviewer=reviewer,
            **validated_data,
        )

    def validate_business_user(self, business_user):
        if (
            business_user.profile.type
            != Profile.UserType.BUSINESS
        ):
            raise serializers.ValidationError(
                "Reviews can only be created for business users."
            )

        return business_user

    def validate(self, attrs):
        reviewer = self.context["request"].user
        business_user = attrs.get("business_user")

        if Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user,
        ).exists():
            raise PermissionDenied(
                "You have already reviewed this business user."
            )

        return attrs

class ReviewUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "business_user",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        allowed_fields = {
            "rating",
            "description",
        }

        submitted_fields = set(
            self.initial_data.keys()
        )

        invalid_fields = (
            submitted_fields - allowed_fields
        )

        if invalid_fields:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Only rating and description "
                        "may be updated."
                    )
                }
            )

        return attrs