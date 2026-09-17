from rest_framework import status

from .base import OfferAPITestBase


class OfferDetailEndpointTests(OfferAPITestBase):

    def test_authenticated_user_can_retrieve_offer_detail(self):
        create_response = self.create_offer()

        detail_id = create_response.data[
            "details"
        ][0]["id"]

        response = self.client.get(
            f"/api/offerdetails/{detail_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            detail_id,
        )
        self.assertEqual(
            response.data["offer_type"],
            "basic",
        )
        self.assertIn(
            "title",
            response.data,
        )
        self.assertIn(
            "price",
            response.data,
        )
        self.assertIn(
            "delivery_time_in_days",
            response.data,
        )
        self.assertIn(
            "features",
            response.data,
        )

    def test_unauthenticated_user_cannot_retrieve_offer_detail(self):
        create_response = self.create_offer()

        detail_id = create_response.data[
            "details"
        ][0]["id"]

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            f"/api/offerdetails/{detail_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unknown_offer_detail_returns_404(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.get(
            "/api/offerdetails/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
