from django.contrib import admin
from django.test import TestCase

from offers.models import Offer, OfferDetail


class OfferAdminTests(TestCase):
    def test_offer_models_are_registered_in_admin(self):
        self.assertIn(Offer, admin.site._registry)
        self.assertIn(OfferDetail, admin.site._registry)