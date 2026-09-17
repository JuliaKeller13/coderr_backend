from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import serializers

from offers.api.serializers import (
    OfferListSerializer,
    OfferWriteSerializer,
)
from offers.models import Offer, OfferDetail
from users.models import Profile


User = get_user_model()


class OfferSerializerEdgeCaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="business",
            password="testpassword",
        )
        Profile.objects.create(
            user=self.user,
            type=Profile.UserType.BUSINESS,
        )
        self.offer = Offer.objects.create(
            user=self.user,
            title="Design",
            description="Design service",
        )

    def _create_detail(self):
        return OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=5,
            price="100.00",
            features=["Logo"],
            offer_type=OfferDetail.OfferType.BASIC,
        )

    def test_metrics_are_calculated_without_annotations(self):
        detail = self._create_detail()
        data = OfferListSerializer(self.offer).data

        self.assertEqual(data["min_price"], 100.0)
        self.assertEqual(data["min_delivery_time"], 5)
        self.assertIn(str(detail.id), data["details"][0]["url"])

    def test_empty_offer_has_no_minimum_values(self):
        data = OfferListSerializer(self.offer).data

        self.assertIsNone(data["min_price"])
        self.assertIsNone(data["min_delivery_time"])

    def test_update_rejects_missing_detail_type(self):
        serializer = OfferWriteSerializer(
            self.offer,
            data={
                "details": [
                    {"offer_type": OfferDetail.OfferType.STANDARD}
                ]
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())

        with self.assertRaises(serializers.ValidationError):
            serializer.save()