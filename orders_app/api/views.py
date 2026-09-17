from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from users_app.models import Profile

from .permissions import (
    IsCustomerUser,
    IsOrderBusinessUser,
)
from .serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,
)

User = get_user_model()


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


class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User,
            pk=business_user_id,
            profile__type=Profile.UserType.BUSINESS,
        )

        order_count = Order.objects.filter(
            business_user=business_user,
            status=Order.Status.IN_PROGRESS,
        ).count()

        return Response(
            {
                "order_count": order_count,
            }
        )


class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User,
            pk=business_user_id,
            profile__type=Profile.UserType.BUSINESS,
        )

        completed_order_count = Order.objects.filter(
            business_user=business_user,
            status=Order.Status.COMPLETED,
        ).count()

        return Response(
            {
                "completed_order_count": (
                    completed_order_count
                ),
            }
        )
