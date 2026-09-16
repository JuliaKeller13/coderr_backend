from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from offers.models import Offer, OfferDetail
from users.models import Profile


User = get_user_model()


class OrderAPITestBase(APITestCase):

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

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Logo Design Offer",
            description="Professional logo design",
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price="150.00",
            features=[
                "Logo Design",
                "Visitenkarten",
            ],
            offer_type=OfferDetail.OfferType.BASIC,
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