from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from users.models import Profile


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

        self.assertEqual(
            User.objects.filter(username="andrey").count(),
            1,
        )
        self.assertEqual(
            User.objects.filter(username="kevin").count(),
            1,
        )
