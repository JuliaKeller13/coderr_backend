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

        customer = self.context[
            "request"
        ].user

        business = offer_detail.offer.user

        return Order.objects.create(
            customer_user=customer,
            business_user=business,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=(
                offer_detail.delivery_time_in_days
            ),
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )