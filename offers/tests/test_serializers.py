from copy import deepcopy

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from offers.api.serializers import OfferWriteSerializer
from offers.models import Offer, OfferDetail
from users.models import Profile

User = get_user_model()


class OfferSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="businessuser",
            email="business@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.user,
            type=Profile.UserType.BUSINESS,
        )

        self.factory = APIRequestFactory()

        self.data = {
            "title": "Grafikdesign-Paket",
            "description": "Professionelles Grafikdesign",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": "100.00",
                    "features": ["Logo Design"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": "200.00",
                    "features": ["Logo Design"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": "500.00",
                    "features": ["Logo Design"],
                    "offer_type": "premium",
                },
            ],
        }

    def get_serializer(self, data):
        request = self.factory.post(
            "/api/offers/"
        )

        request.user = self.user

        return OfferWriteSerializer(
            data=data,
            context={
                "request": request,
            },
        )

    def test_serializer_creates_offer_with_three_details(self):
        serializer = self.get_serializer(
            deepcopy(self.data)
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        offer = serializer.save()

        self.assertEqual(
            Offer.objects.count(),
            1,
        )
        self.assertEqual(
            OfferDetail.objects.count(),
            3,
        )
        self.assertEqual(
            offer.user,
            self.user,
        )
        self.assertEqual(
            offer.details.count(),
            3,
        )

    def test_serializer_requires_exactly_three_details(self):
        data = deepcopy(self.data)
        data["details"] = data["details"][:2]

        serializer = self.get_serializer(data)

        self.assertFalse(
            serializer.is_valid()
        )
        self.assertIn(
            "details",
            serializer.errors,
        )

    def test_serializer_requires_all_offer_types(self):
        data = deepcopy(self.data)

        data["details"][1]["offer_type"] = "basic"

        serializer = self.get_serializer(data)

        self.assertFalse(
            serializer.is_valid()
        )
        self.assertIn(
            "details",
            serializer.errors,
        )
