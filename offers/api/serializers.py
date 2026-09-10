from rest_framework import serializers

from offers.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

        read_only_fields = [
            "id",
        ]

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(
        many=True,
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        user = self.context["request"].user

        offer = Offer.objects.create(
            user=user,
            **validated_data,
        )

        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data,
            )

        return offer

    def validate_details(self, details):
        required_types = {
            OfferDetail.OfferType.BASIC,
            OfferDetail.OfferType.STANDARD,
            OfferDetail.OfferType.PREMIUM,
        }

        offer_types = {
            detail["offer_type"]
            for detail in details
        }

        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly three details."
            )

        if offer_types != required_types:
            raise serializers.ValidationError(
                "Details must contain basic, standard and premium."
            )

        return details