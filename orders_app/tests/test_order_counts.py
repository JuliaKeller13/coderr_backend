from rest_framework import status

from orders_app.models import Order

from .base import OrderAPITestBase


class OrderCountTests(OrderAPITestBase):

    def create_order(
        self,
        status_value=Order.Status.IN_PROGRESS,
        business=None,
    ):
        return Order.objects.create(
            customer_user=self.customer_user,
            business_user=business or self.business_user,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price="150.00",
            features=["Logo Design"],
            offer_type="basic",
            status=status_value,
        )

    def test_order_count_returns_in_progress_orders(self):
        self.create_order()
        self.create_order()

        self.create_order(
            status_value=Order.Status.COMPLETED
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            f"/api/order-count/{self.business_user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["order_count"],
            2,
        )

    def test_completed_order_count_returns_completed_orders(self):
        self.create_order(
            status_value=Order.Status.COMPLETED
        )
        self.create_order(
            status_value=Order.Status.COMPLETED
        )
        self.create_order()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(

                "/api/completed-order-count/"
                f"{self.business_user.id}/"

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["completed_order_count"],
            2,
        )

    def test_order_count_only_counts_requested_business_user(self):
        other_business = self.create_business_user(
            username="otherbusiness"
        )

        self.create_order()
        self.create_order(
            business=other_business
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            f"/api/order-count/{self.business_user.id}/"
        )

        self.assertEqual(
            response.data["order_count"],
            1,
        )

    def test_order_count_requires_authentication(self):
        response = self.client.get(
            f"/api/order-count/{self.business_user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_completed_order_count_requires_authentication(self):
        response = self.client.get(

                "/api/completed-order-count/"
                f"{self.business_user.id}/"

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_order_count_unknown_business_user_returns_404(self):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/order-count/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_completed_order_count_unknown_business_user_returns_404(
        self,
    ):
        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/completed-order-count/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_customer_id_is_not_valid_business_user(self):
        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.get(
            f"/api/order-count/{self.customer_user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
