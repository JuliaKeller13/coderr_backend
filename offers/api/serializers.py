from django.db.models import Min
from django.urls import reverse
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


class OfferDetailReferenceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):
        url = reverse(
            "offer-detail-item",
            kwargs={"pk": obj.pk},
        )

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(url)

        return url


class OfferWriteSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

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


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailReferenceSerializer(
        many=True,
        read_only=True,
    )

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

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
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        value = getattr(obj, "min_price", None)

        if value is None:
            value = obj.details.aggregate(
                minimum=Min("price")
            )["minimum"]

        if value is None:
            return None

        return float(value)

    def get_min_delivery_time(self, obj):
        value = getattr(
            obj,
            "min_delivery_time",
            None,
        )

        if value is None:
            value = obj.details.aggregate(
                minimum=Min("delivery_time_in_days")
            )["minimum"]

        return value

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }