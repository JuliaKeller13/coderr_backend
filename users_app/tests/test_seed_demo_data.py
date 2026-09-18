from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import models
from django.test import TestCase

from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review
from users_app.models import Profile


class SeedDemoDataTests(TestCase):
    def test_creates_customer_and_business_guest_users(self):
        call_command("seed_demo_data")

        customer = User.objects.get(username="andrey")
        business = User.objects.get(username="kevin")

        self.assertEqual(
            customer.profile.type,
            Profile.UserType.CUSTOMER,
        )
        self.assertEqual(
            business.profile.type,
            Profile.UserType.BUSINESS,
        )
        self.assertTrue(customer.check_password("asdasd"))
        self.assertTrue(business.check_password("asdasd24"))

    def test_seed_demo_data_can_run_multiple_times(self):
        call_command("seed_demo_data")
        call_command("seed_demo_data")

        self.assertEqual(User.objects.count(), 6)
        self.assertEqual(Offer.objects.count(), 6)
        self.assertEqual(Order.objects.count(), 6)
        self.assertEqual(Review.objects.count(), 6)

    def test_creates_expected_demo_profiles(self):
        call_command("seed_demo_data")

        self.assertEqual(
            Profile.objects.filter(type=Profile.UserType.CUSTOMER).count(),
            3,
        )
        self.assertEqual(
            Profile.objects.filter(type=Profile.UserType.BUSINESS).count(),
            3,
        )
        self.assertTrue(User.objects.get(username="kevin").profile.tel)

    def test_creates_offers_with_three_details_each(self):
        call_command("seed_demo_data")

        self.assertEqual(Offer.objects.count(), 6)
        self.assertTrue(
            all(offer.details.count() == 3 for offer in Offer.objects.all())
        )

    def test_creates_orders_with_multiple_statuses(self):
        call_command("seed_demo_data")

        self.assertEqual(Order.objects.count(), 6)
        self.assertGreaterEqual(Order.objects.values("status").distinct().count(), 3)

    def test_creates_valid_reviews(self):
        call_command("seed_demo_data")

        self.assertEqual(Review.objects.count(), 6)
        self.assertTrue(all(1 <= review.rating <= 5 for review in Review.objects.all()))
        self.assertFalse(
            Review.objects.filter(reviewer=models.F("business_user")).exists()
        )
