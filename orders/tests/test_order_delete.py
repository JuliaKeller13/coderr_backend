from django.contrib.auth import get_user_model
from rest_framework import status

from orders.models import Order

from .base import OrderAPITestBase


User = get_user_model()


class OrderDeleteTests(OrderAPITestBase):

    def create_order(self):
        return Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
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

    def create_staff_user(self):
        return User.objects.create_user(
            username="admin",
            password="testpassword",
            is_staff=True,
        )

    def test_staff_user_can_delete_order(self):
        order = self.create_order()

        staff_user = self.create_staff_user()

        self.client.force_authenticate(
            user=staff_user
        )

        response = self.client.delete(
            f"/api/orders/{order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Order.objects.filter(
                pk=order.id
            ).exists()
        )

    def test_business_user_cannot_delete_order(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.delete(
            f"/api/orders/{order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Order.objects.filter(
                pk=order.id
            ).exists()
        )

    def test_customer_user_cannot_delete_order(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.delete(
            f"/api/orders/{order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_delete_order(self):
        order = self.create_order()

        response = self.client.delete(
            f"/api/orders/{order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_unknown_order_returns_404(self):
        staff_user = self.create_staff_user()

        self.client.force_authenticate(
            user=staff_user
        )

        response = self.client.delete(
            "/api/orders/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )