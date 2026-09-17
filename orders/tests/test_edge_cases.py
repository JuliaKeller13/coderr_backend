from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from orders.api.permissions import IsOrderBusinessUser
from orders.api.views import OrderListCreateView
from orders.models import Order

from .base import OrderAPITestBase


class OrderEdgeCaseTests(OrderAPITestBase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price="150.00",
            features=["Logo Design"],
            offer_type="basic",
        )

    def test_business_owner_has_object_permission(self):
        request = self.factory.patch(
            "/api/orders/1/"
        )
        request.user = self.business_user

        permission = IsOrderBusinessUser()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.order,
            )
        )

    def test_anonymous_user_has_no_object_permission(self):
        request = self.factory.patch(
            "/api/orders/1/"
        )
        request.user = AnonymousUser()

        permission = IsOrderBusinessUser()

        self.assertFalse(
            permission.has_object_permission(
                request,
                None,
                self.order,
            )
        )

    def test_anonymous_user_gets_empty_queryset(self):
        request = self.factory.get(
            "/api/orders/"
        )
        request.user = AnonymousUser()

        view = OrderListCreateView()
        view.request = request

        self.assertFalse(
            view.get_queryset().exists()
        )
