from rest_framework import status

from orders.models import Order

from .base import OrderAPITestBase


class OrderUpdateTests(OrderAPITestBase):

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

    def test_business_user_can_update_order_status(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            Order.Status.COMPLETED,
        )

        self.assertEqual(
            response.data["status"],
            "completed",
        )

    def test_customer_cannot_update_order(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_other_business_cannot_update_order(self):
        order = self.create_order()

        other_business = self.create_business_user(
            username="otherbusiness"
        )

        self.client.force_authenticate(
            user=other_business
        )

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_update_order(self):
        order = self.create_order()

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_invalid_status_returns_400(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "status": "something_wrong",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_other_fields_cannot_be_updated(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.patch(
            f"/api/orders/{order.id}/",
            {
                "title": "Hacked Title",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        order.refresh_from_db()

        self.assertEqual(
            order.title,
            "Logo Design",
        )

    def test_unknown_order_returns_404(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.patch(
            "/api/orders/99999/",
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
