from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from users.models import Profile


User = get_user_model()


class ReviewAPITestBase(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.customer_user,
            type=Profile.UserType.CUSTOMER,
        )

        self.business_user = User.objects.create_user(
            username="business",
            password="testpassword",
        )

        Profile.objects.create(
            user=self.business_user,
            type=Profile.UserType.BUSINESS,
        )

    def create_customer_user(
        self,
        username="othercustomer",
    ):
        user = User.objects.create_user(
            username=username,
            password="testpassword",
        )

        Profile.objects.create(
            user=user,
            type=Profile.UserType.CUSTOMER,
        )

        return user


    def create_business_user(
        self,
        username="otherbusiness",
    ):
        user = User.objects.create_user(
            username=username,
            password="testpassword",
        )

        Profile.objects.create(
            user=user,
            type=Profile.UserType.BUSINESS,
        )

        return user