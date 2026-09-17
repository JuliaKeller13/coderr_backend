from copy import deepcopy

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users_app.models import Profile

User = get_user_model()


class OfferAPITestBase(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business",
            email="business@example.com",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        )

        Profile.objects.create(
            user=self.business_user,
            type=Profile.UserType.BUSINESS,
        )

        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.customer_user,
            type=Profile.UserType.CUSTOMER,
        )

        self.offer_data = {
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
                    "delivery_time_in_days": 7,
                    "price": "200.00",
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                    ],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": "500.00",
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

    def create_offer(self, data=None, user=None):
        if user is None:
            user = self.business_user

        if data is None:
            data = self.offer_data

        self.client.force_authenticate(user=user)

        return self.client.post(
            "/api/offers/",
            deepcopy(data),
            format="json",
        )

    def create_business_user(
        self,
        username="otherbusiness",
    ):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="testpassword",
        )

        Profile.objects.create(
            user=user,
            type=Profile.UserType.BUSINESS,
        )

        return user
