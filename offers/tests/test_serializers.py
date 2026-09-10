from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from offers.api.serializers import OfferSerializer
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

    def test_offer_serializer_creates_offer_with_three_details(self):
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Professionelles Grafikdesign",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": "100.00",
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                    ],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 3,
                    "price": "200.00",
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Flyer",
                    ],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": -1,
                    "delivery_time_in_days": 1,
                    "price": "500.00",
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Flyer",
                        "Source files",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

        request = self.factory.post("/api/offers/")
        request.user = self.user

        serializer = OfferSerializer(
            data=data,
            context={"request": request},
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        offer = serializer.save()

        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(OfferDetail.objects.count(), 3)
        self.assertEqual(offer.user, self.user)
        self.assertEqual(offer.details.count(), 3)

    def test_offer_requires_exactly_three_details(self):
        data = {
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
                    "delivery_time_in_days": 3,
                    "price": "200.00",
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "standard",
                },
            ],
        }

        request = self.factory.post("/api/offers/")
        request.user = self.user

        serializer = OfferSerializer(
            data=data,
            context={"request": request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("details", serializer.errors)


    def test_offer_requires_basic_standard_and_premium(self):
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Professionelles Grafikdesign",
            "details": [
                {
                    "title": "Basic 1",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": "100.00",
                    "features": ["Logo"],
                    "offer_type": "basic",
                },
                {
                    "title": "Basic 2",
                    "revisions": 3,
                    "delivery_time_in_days": 4,
                    "price": "150.00",
                    "features": ["Logo", "PNG"],
                    "offer_type": "basic",
                },
                {
                    "title": "Premium",
                    "revisions": -1,
                    "delivery_time_in_days": 1,
                    "price": "500.00",
                    "features": ["Logo", "Source files"],
                    "offer_type": "premium",
                },
            ],
        }

        request = self.factory.post("/api/offers/")
        request.user = self.user

        serializer = OfferSerializer(
            data=data,
            context={"request": request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("details", serializer.errors)