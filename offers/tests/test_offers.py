from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from offers.models import Offer
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

    def create_offer(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        return self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

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

    def test_offer_list_contains_expected_fields(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        create_response = self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/"
        )

        offer = response.data["results"][0]

        self.assertIn("id", offer)
        self.assertIn("user", offer)
        self.assertIn("title", offer)
        self.assertIn("image", offer)
        self.assertIn("description", offer)
        self.assertIn("created_at", offer)
        self.assertIn("updated_at", offer)
        self.assertIn("details", offer)
        self.assertIn("min_price", offer)
        self.assertIn("min_delivery_time", offer)
        self.assertIn("user_details", offer)

    def test_offer_list_returns_min_price_and_delivery_time(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        self.client.post(
            "/api/offers/",
            self.offer_data,
            format="json",
        )

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/"
        )

        offer = response.data["results"][0]

        self.assertEqual(
            offer["min_price"],
            100.0,
        )

        self.assertEqual(
            offer["min_delivery_time"],
            1,
        )

    def test_filter_by_creator_id(self):
        self.create_offer()

        self.client.force_authenticate(user=None)

        response = self.client.get(
            f"/api/offers/?creator_id={self.business_user.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )


    def test_filter_by_min_price(self):
        self.create_offer()

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/?min_price=100"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_filter_by_max_delivery_time(self):
        self.create_offer()

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/?max_delivery_time=5"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )


    def test_search_offers(self):
        self.create_offer()

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/?search=Grafikdesign"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )


    def test_ordering_by_min_price(self):
        self.create_offer()

        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/offers/?ordering=min_price"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_authenticated_user_can_retrieve_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        response = self.client.get(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            offer_id,
        )

        self.assertEqual(
            response.data["title"],
            "Grafikdesign-Paket",
        )

        self.assertIn(
            "details",
            response.data,
        )

        self.assertIn(
            "min_price",
            response.data,
        )

        self.assertIn(
            "min_delivery_time",
            response.data,
        )

    def test_unauthenticated_user_cannot_retrieve_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        self.client.force_authenticate(user=None)

        response = self.client.get(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_owner_can_patch_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        response = self.client.patch(
            f"/api/offers/{offer_id}/",
            {
                "title": "Updated Grafikdesign-Paket",
                "details": [
                    {
                        "offer_type": "basic",
                        "title": "Basic Updated",
                        "price": "120.00",
                        "revisions": 3,
                        "delivery_time_in_days": 4,
                        "features": ["Logo", "PNG"],
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Updated Grafikdesign-Paket",
        )

    def test_non_owner_cannot_patch_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        other_user = User.objects.create_user(
            username="otherbusiness",
            password="testpassword",
        )

        Profile.objects.create(
            user=other_user,
            type=Profile.UserType.BUSINESS,
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.patch(
            f"/api/offers/{offer_id}/",
            {
                "title": "Forbidden Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_owner_can_delete_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        response = self.client.delete(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Offer.objects.filter(
                pk=offer_id
            ).exists()
        )