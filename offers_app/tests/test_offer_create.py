from copy import deepcopy

from rest_framework import status

from offers_app.models import Offer, OfferDetail

from .base import OfferAPITestBase


class OfferCreateTests(OfferAPITestBase):

    def test_business_user_can_create_offer(self):
        response = self.create_offer()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Offer.objects.count(),
            1,
        )
        self.assertEqual(
            OfferDetail.objects.count(),
            3,
        )

        self.assertEqual(
            len(response.data["details"]),
            3,
        )

    def test_customer_user_cannot_create_offer(self):
        response = self.create_offer(
            user=self.customer_user
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Offer.objects.count(),
            0,
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

    def test_invalid_offer_data_returns_400(self):
        data = deepcopy(self.offer_data)

        data["details"] = data["details"][:2]

        response = self.create_offer(
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
