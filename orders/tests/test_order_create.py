from decimal import Decimal

from rest_framework import status

from orders.models import Order

from .base import OrderAPITestBase


class OrderCreateTests(OrderAPITestBase):
    def test_customer_can_create_order(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Order.objects.count(),
            1,
        )

        order = Order.objects.first()

        self.assertEqual(
            order.customer_user,
            self.customer_user,
        )
        self.assertEqual(
            order.business_user,
            self.business_user,
        )
        self.assertEqual(
            order.title,
            self.offer_detail.title,
        )
        self.assertEqual(
            order.price,
            Decimal("150.00"),
        )
        self.assertEqual(
            order.status,
            Order.Status.IN_PROGRESS,
        )

    def test_business_user_cannot_create_order(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_create_order(self):
        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": self.offer_detail.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_missing_offer_detail_id_returns_400(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/orders/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unknown_offer_detail_returns_404(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.post(
            "/api/orders/",
            {
                "offer_detail_id": 99999,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )