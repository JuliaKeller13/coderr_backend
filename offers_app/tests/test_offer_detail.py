from rest_framework import status

from offers_app.models import Offer, OfferDetail

from .base import OfferAPITestBase


class OfferDetailTests(OfferAPITestBase):

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

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unknown_offer_returns_404(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.get(
            "/api/offers/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_owner_can_patch_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        response = self.client.patch(
            f"/api/offers/{offer_id}/",
            {
                "title": "Updated Grafikdesign-Paket",
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

        offer = Offer.objects.get(
            pk=offer_id
        )

        self.assertEqual(
            offer.title,
            "Updated Grafikdesign-Paket",
        )

    def test_patch_only_updates_requested_detail(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        offer = Offer.objects.get(
            pk=offer_id
        )

        basic = offer.details.get(
            offer_type=OfferDetail.OfferType.BASIC
        )
        standard = offer.details.get(
            offer_type=OfferDetail.OfferType.STANDARD
        )
        premium = offer.details.get(
            offer_type=OfferDetail.OfferType.PREMIUM
        )

        original_standard_price = standard.price
        original_premium_price = premium.price

        response = self.client.patch(
            f"/api/offers/{offer_id}/",
            {
                "details": [
                    {
                        "offer_type": "basic",
                        "price": "120.00",
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        basic.refresh_from_db()
        standard.refresh_from_db()
        premium.refresh_from_db()

        self.assertEqual(
            float(basic.price),
            120.0,
        )
        self.assertEqual(
            standard.price,
            original_standard_price,
        )
        self.assertEqual(
            premium.price,
            original_premium_price,
        )

    def test_non_owner_cannot_patch_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        other_user = self.create_business_user()

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

    def test_unauthenticated_user_cannot_patch_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        self.client.force_authenticate(
            user=None
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
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_patch_unknown_offer_returns_404(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.patch(
            "/api/offers/99999/",
            {
                "title": "Unknown",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_patch_returns_400(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        response = self.client.patch(
            f"/api/offers/{offer_id}/",
            {
                "details": [
                    {
                        "offer_type": "invalid",
                        "price": "120.00",
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
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
        self.assertIsNone(
            response.data
        )
        self.assertFalse(
            Offer.objects.filter(
                pk=offer_id
            ).exists()
        )

    def test_non_owner_cannot_delete_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        other_user = self.create_business_user(
            username="deleteuser"
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.delete(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Offer.objects.filter(
                pk=offer_id
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_offer(self):
        create_response = self.create_offer()
        offer_id = create_response.data["id"]

        self.client.force_authenticate(
            user=None
        )

        response = self.client.delete(
            f"/api/offers/{offer_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_unknown_offer_returns_404(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.delete(
            "/api/offers/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
