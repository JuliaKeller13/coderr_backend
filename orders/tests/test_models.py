from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order

User = get_user_model()


class OrderModelTests(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="testpassword",
        )

        self.business = User.objects.create_user(
            username="business",
            password="testpassword",
        )

    def test_order_can_be_created(self):
        order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price="150.00",
            features=[
                "Logo Design",
                "Visitenkarten",
            ],
            offer_type="basic",
        )

        self.assertEqual(
            order.customer_user,
            self.customer,
        )

        self.assertEqual(
            order.business_user,
            self.business,
        )

        self.assertEqual(
            order.title,
            "Logo Design",
        )

        self.assertEqual(
            order.status,
            Order.Status.IN_PROGRESS,
        )

        self.assertEqual(
            str(order),
            "Logo Design - in_progress",
        )
