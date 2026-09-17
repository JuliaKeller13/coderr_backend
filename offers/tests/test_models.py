from django.contrib.auth import get_user_model
from django.test import TestCase

from offers.models import Offer, OfferDetail
from users.models import Profile

User = get_user_model()


class OfferModelTests(TestCase):

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

    def test_offer_can_be_created(self):
        offer = Offer.objects.create(
            user=self.user,
            title="Grafikdesign-Paket",
            description="Professionelles Grafikdesign",
        )

        self.assertEqual(offer.user, self.user)
        self.assertEqual(
            offer.title,
            "Grafikdesign-Paket",
        )
        self.assertEqual(
            offer.description,
            "Professionelles Grafikdesign",
        )

        self.assertEqual(
            str(offer),
            "Grafikdesign-Paket",
        )

    def test_offer_detail_is_linked_to_offer(self):
        offer = Offer.objects.create(
            user=self.user,
            title="Grafikdesign-Paket",
            description="Professionelles Grafikdesign",
        )

        detail = OfferDetail.objects.create(
            offer=offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price="100.00",
            features=[
                "Logo Design",
                "Visitenkarte",
            ],
            offer_type=OfferDetail.OfferType.BASIC,
        )

        self.assertEqual(detail.offer, offer)
        self.assertEqual(
            detail.offer_type,
            OfferDetail.OfferType.BASIC,
        )
        self.assertEqual(
            offer.details.count(),
            1,
        )

        self.assertEqual(
            str(detail),
            "Grafikdesign-Paket - basic",
        )
