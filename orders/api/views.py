from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from orders.models import Order

from .permissions import (
    IsCustomerUser,
    IsOrderBusinessUser,
)
from .serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,
)


class OrderListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Order.objects.none()

        return Order.objects.filter(
            Q(customer_user=user)
            | Q(business_user=user)
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerUser()]

        return [IsAuthenticated()]

class OrderUpdateView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer

    http_method_names = [
        "patch",
        "delete",
        "options",
    ]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsAdminUser(),
            ]

        return [
            IsAuthenticated(),
            IsOrderBusinessUser(),
        ]