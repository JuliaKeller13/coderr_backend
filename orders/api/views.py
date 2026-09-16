from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order

from .permissions import IsCustomerUser
from .serializers import OrderSerializer


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
