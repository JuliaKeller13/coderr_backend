from rest_framework import serializers

from reviews.models import Review


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