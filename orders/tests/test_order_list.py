from rest_framework import status

from orders.models import Order

from .base import OrderAPITestBase


class OrderListTests(OrderAPITestBase):

    def create_order(
        self,
        customer=None,
        business=None,
        title="Logo Design",
    ):
        return Order.objects.create(
            customer_user=customer or self.customer_user,
            business_user=business or self.business_user,
            title=title,
            revisions=3,
            delivery_time_in_days=5,
            price="150.00",
            features=[
                "Logo Design",
                "Visitenkarten",
            ],
            offer_type="basic",
        )

    def test_customer_can_see_own_orders(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            order.id,
        )

    def test_business_user_can_see_own_orders(self):
        order = self.create_order()

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            order.id,
        )

    def test_user_cannot_see_unrelated_orders(self):
        other_customer = self.create_customer_user(
            username="othercustomer"
        )

        other_business = self.create_business_user(
            username="otherbusiness"
        )

        self.create_order(
            customer=other_customer,
            business=other_business,
            title="Unrelated Order",
        )

        own_order = self.create_order(
            title="Own Order",
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            own_order.id,
        )

    def test_unauthenticated_user_cannot_list_orders(self):
        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
