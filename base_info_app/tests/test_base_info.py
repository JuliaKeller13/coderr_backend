from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer
from reviews_app.models import Review
from users_app.models import Profile

User = get_user_model()


class BaseInfoTests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.business_user,
            type=Profile.UserType.BUSINESS,
        )

        self.customer_user = User.objects.create_user(
            username="customer",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.customer_user,
            type=Profile.UserType.CUSTOMER,
        )

        Offer.objects.create(
            user=self.business_user,
            title="Logo Design",
            description="Professional logo design",
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr gut.",
        )

    def test_base_info_returns_platform_statistics(self):
        response = self.client.get(
            "/api/base-info/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["review_count"],
            1,
        )

        self.assertEqual(
            response.data["average_rating"],
            4.0,
        )

        self.assertEqual(
            response.data["business_profile_count"],
            1,
        )

        self.assertEqual(
            response.data["offer_count"],
            1,
        )

    def test_base_info_does_not_require_authentication(self):
        response = self.client.get(
            "/api/base-info/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_average_rating_is_rounded_to_one_decimal_place(self):
        second_customer = User.objects.create_user(
            username="customer2",
            password="testpassword",
        )

        Profile.objects.create(
            user=second_customer,
            type=Profile.UserType.CUSTOMER,
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=second_customer,
            rating=5,
            description="Top!",
        )

        response = self.client.get(
            "/api/base-info/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["average_rating"],
            4.5,
        )

    def test_average_rating_is_zero_when_no_reviews_exist(self):
        Review.objects.all().delete()

        response = self.client.get(
            "/api/base-info/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["review_count"],
            0,
        )

        self.assertEqual(
            response.data["average_rating"],
            0.0,
        )
