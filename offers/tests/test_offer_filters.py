from copy import deepcopy
from datetime import timedelta

from django.utils import timezone
from rest_framework import status

from offers.models import Offer

from .base import OfferAPITestBase


class OfferFilterTests(OfferAPITestBase):

    def test_filter_by_creator_id(self):
        self.create_offer()

        other_user = self.create_business_user()
        other_data = deepcopy(self.offer_data)
        other_data["title"] = "Other Offer"

        self.create_offer(
            data=other_data,
            user=other_user,
        )

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            (
                "/api/offers/"
                f"?creator_id={self.business_user.id}"
            )
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

        expensive = deepcopy(self.offer_data)
        expensive["title"] = "Expensive Offer"

        expensive["details"][0]["price"] = "300.00"
        expensive["details"][1]["price"] = "400.00"
        expensive["details"][2]["price"] = "500.00"

        self.create_offer(
            data=expensive
        )

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?min_price=200"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )
        self.assertEqual(
            response.data["results"][0]["title"],
            "Expensive Offer",
        )

    def test_filter_by_max_delivery_time(self):
        self.create_offer()

        slow_offer = deepcopy(self.offer_data)
        slow_offer["title"] = "Slow Offer"

        slow_offer["details"][0][
            "delivery_time_in_days"
        ] = 8
        slow_offer["details"][1][
            "delivery_time_in_days"
        ] = 9
        slow_offer["details"][2][
            "delivery_time_in_days"
        ] = 10

        self.create_offer(
            data=slow_offer
        )

        self.client.force_authenticate(
            user=None
        )

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
        self.assertEqual(
            response.data["results"][0]["title"],
            "Grafikdesign-Paket",
        )

    def test_search_by_title(self):
        self.create_offer()

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?search=Grafikdesign"
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_search_by_description(self):
        self.create_offer()

        other_data = deepcopy(self.offer_data)
        other_data["title"] = "Illustration Package"
        other_data["description"] = (
            "Spezielle Illustrationen für Unternehmen"
        )

        self.create_offer(
            data=other_data
        )

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?search=Illustrationen"
        )

        self.assertEqual(
            response.data["count"],
            1,
        )
        self.assertEqual(
            response.data["results"][0]["title"],
            "Illustration Package",
        )

    def test_ordering_by_min_price(self):
        expensive = deepcopy(self.offer_data)
        expensive["title"] = "Expensive Offer"

        expensive["details"][0]["price"] = "300.00"
        expensive["details"][1]["price"] = "400.00"
        expensive["details"][2]["price"] = "500.00"

        self.create_offer(
            data=expensive
        )
        self.create_offer()

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?ordering=min_price"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Grafikdesign-Paket",
        )
        self.assertEqual(
            response.data["results"][1]["title"],
            "Expensive Offer",
        )

    def test_ordering_by_updated_at_descending(self):
        first_response = self.create_offer()

        second_data = deepcopy(self.offer_data)
        second_data["title"] = "Newer Offer"

        second_response = self.create_offer(
            data=second_data
        )

        first_offer = Offer.objects.get(
            pk=first_response.data["id"]
        )
        second_offer = Offer.objects.get(
            pk=second_response.data["id"]
        )

        now = timezone.now()

        Offer.objects.filter(
            pk=first_offer.pk
        ).update(
            updated_at=now - timedelta(days=1)
        )

        Offer.objects.filter(
            pk=second_offer.pk
        ).update(
            updated_at=now
        )

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/offers/?ordering=-updated_at"
        )

        self.assertEqual(
            response.data["results"][0]["id"],
            second_offer.id,
        )
        self.assertEqual(
            response.data["results"][1]["id"],
            first_offer.id,
        )

    def test_invalid_numeric_filter_returns_400(self):
        queries = [
            "creator_id=invalid",
            "min_price=invalid",
            "max_delivery_time=invalid",
        ]

        for query in queries:
            with self.subTest(query=query):
                response = self.client.get(
                    f"/api/offers/?{query}"
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )