from rest_framework import status

from .base import OfferAPITestBase


class OfferListTests(OfferAPITestBase):

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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn(
            "count",
            response.data,
        )
        self.assertIn(
            "results",
            response.data,
        )

    def test_page_size_limits_results(self):
        for _ in range(7):
            self.create_offer()

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?page_size=3"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            7,
        )
        self.assertEqual(
            len(response.data["results"]),
            3,
        )

    def test_offer_list_contains_expected_data(self):
        self.create_offer()

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/"
        )

        offer = response.data["results"][0]

        expected_fields = {
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
        }

        self.assertTrue(
            expected_fields.issubset(
                offer.keys()
            )
        )

        self.assertEqual(
            offer["min_price"],
            100.0,
        )
        self.assertEqual(
            offer["min_delivery_time"],
            5,
        )

        self.assertEqual(
            offer["user_details"]["first_name"],
            "John",
        )
        self.assertEqual(
            offer["user_details"]["last_name"],
            "Doe",
        )
        self.assertEqual(
            offer["user_details"]["username"],
            "business",
        )

        self.assertEqual(
            len(offer["details"]),
            3,
        )

        first_detail = offer["details"][0]

        self.assertIn(
            "id",
            first_detail,
        )
        self.assertIn(
            "url",
            first_detail,
        )

        self.assertTrue(
            first_detail["url"].endswith(
                f"/api/offerdetails/{first_detail['id']}/"
            )
        )