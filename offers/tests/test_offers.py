from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile


User = get_user_model()


class OfferAPITests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business",
            email="business@example.com",
            password="testpassword",
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
                {
                    "title": "Premium Design",
                    "revisions": -1,
                    "delivery_time_in_days": 1,
                    "price": "500.00",
                    "features": ["Logo Design", "Source files"],
                    "offer_type": "premium",
                },
            ],
        }

    def test_business_user_can_create_offer(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_customer_user_cannot_create_offer(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_create_offer(self):
        response = self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_offer_list_is_public(self):
        response = self.client.get(
            "/api/offers/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_offer_list_is_paginated(self):
        response = self.client.get(
            "/api/offers/"
        )

        self.assertIn(
            "count",
            response.data,
        )

        self.assertIn(
            "results",
            response.data,
        )