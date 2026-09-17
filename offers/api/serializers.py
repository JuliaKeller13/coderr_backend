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
        if self.instance is None:
            self._validate_detail_count(details)
            self._validate_detail_types(details)

        return details

    @staticmethod
    def _validate_detail_count(details):
        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly three details."
            )

    @staticmethod
    def _validate_detail_types(details):
        required_types = {
            OfferDetail.OfferType.BASIC,
            OfferDetail.OfferType.STANDARD,
            OfferDetail.OfferType.PREMIUM,
        }
        offer_types = {
            detail["offer_type"] for detail in details
        }

        if offer_types != required_types:
            raise serializers.ValidationError(
                "Details must contain basic, standard and premium."
            )

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user
        offer = Offer.objects.create(
            user=user,
            **validated_data,
        )
        self._create_details(offer, details_data)
        return offer

    @staticmethod
    def _create_details(offer, details_data):
        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data,
            )

    def update(self, instance, validated_data):
        details_data = validated_data.pop(
            "details",
            None,
        )
        instance = super().update(
            instance,
            validated_data,
        )

        if details_data is not None:
            self._update_details(instance, details_data)

        return instance

    def _update_details(self, instance, details_data):
        existing_details = {
            detail.offer_type: detail
            for detail in instance.details.all()
        }

        for detail_data in details_data:
            self._update_detail(
                existing_details,
                detail_data,
            )

    def _update_detail(self, existing_details, detail_data):
        offer_type = detail_data.pop("offer_type")
        detail = existing_details.get(offer_type)

        if detail is None:
            self._raise_missing_detail(offer_type)

        self._set_detail_fields(detail, detail_data)
        detail.save()

    @staticmethod
    def _set_detail_fields(detail, detail_data):
        for field, value in detail_data.items():
            setattr(detail, field, value)

    @staticmethod
    def _raise_missing_detail(offer_type):
        raise serializers.ValidationError(
            {
                "details": (
                    "No detail with offer_type "
                    f"'{offer_type}' exists."
                )
            }
        )


class OfferMetricsMixin:
    @staticmethod
    def _get_minimum(obj, attribute, field):
        value = getattr(obj, attribute, None)

        if value is None:
            value = obj.details.aggregate(
                minimum=Min(field)
            )["minimum"]

        return value

    def get_min_price(self, obj):
        value = self._get_minimum(
            obj,
            "min_price",
            "price",
        )

        if value is None:
            return None

        return float(value)

    def get_min_delivery_time(self, obj):
        return self._get_minimum(
            obj,
            "min_delivery_time",
            "delivery_time_in_days",
        )


class OfferListSerializer(
    OfferMetricsMixin,
    serializers.ModelSerializer,
):
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

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }


class OfferDetailViewSerializer(
    OfferMetricsMixin,
    serializers.ModelSerializer,
):
    details = OfferDetailReferenceSerializer(
        many=True,
        read_only=True,
    )
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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
        ]
