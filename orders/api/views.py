from rest_framework import generics

from orders.models import Order

from .permissions import IsCustomerUser
from .serializers import OrderSerializer


class OrderListCreateView(
    generics.ListCreateAPIView
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerUser()]

        return super().get_permissions()