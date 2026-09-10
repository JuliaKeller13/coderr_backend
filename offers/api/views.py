from django.db.models import Min
from rest_framework import generics

from offers.models import Offer, OfferDetail

from .pagination import OfferPagination
from .permissions import IsBusinessUser
from .serializers import (
    OfferDetailSerializer,
    OfferListSerializer,
    OfferWriteSerializer,
)


class OfferDetailRetrieveView(
    generics.RetrieveAPIView
):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []


class OfferListCreateView(generics.ListCreateAPIView):
    pagination_class = OfferPagination

    def get_queryset(self):
        return (
            Offer.objects
            .select_related("user")
            .prefetch_related("details")
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min(
                    "details__delivery_time_in_days"
                ),
            )
            .order_by("-updated_at")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferWriteSerializer

        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []
