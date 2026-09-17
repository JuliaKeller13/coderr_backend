from rest_framework import serializers
from rest_framework.exceptions import NotFound

from offers.models import OfferDetail
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            "offer_detail_id",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_offer_detail_id(
        self,
        offer_detail_id,
    ):
        try:
            return OfferDetail.objects.get(
                pk=offer_detail_id
            )
        except OfferDetail.DoesNotExist:
            raise NotFound(
                "Offer detail not found."
            )

    def create(self, validated_data):
        offer_detail = validated_data.pop(
            "offer_detail_id"
        )
        customer = self.context["request"].user
        order_data = self._get_order_data(
            customer,
            offer_detail,
        )
        return Order.objects.create(**order_data)

    @staticmethod
    def _get_order_data(customer, offer_detail):
        return {
            "customer_user": customer,
            "business_user": offer_detail.offer.user,
            "title": offer_detail.title,
            "revisions": offer_detail.revisions,
            "delivery_time_in_days": offer_detail.delivery_time_in_days,
            "price": offer_detail.price,
            "features": offer_detail.features,
            "offer_type": offer_detail.offer_type,
        }


class OrderStatusUpdateSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        invalid_fields = self._get_invalid_fields()

        if invalid_fields:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Only the status field "
                        "may be updated."
                    )
                }
            )

        return attrs

    def _get_invalid_fields(self):
        allowed_fields = {"status"}
        submitted_fields = set(self.initial_data.keys())
        return submitted_fields - allowed_fields