from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from offers.models import Offer, OfferDetail
from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import (
    IsBusinessUser,
    IsOfferOwnerOrReadOnly,
)
from .serializers import (
    OfferDetailSerializer,
    OfferDetailViewSerializer,
    OfferListSerializer,
    OfferWriteSerializer,
)


class OfferDetailRetrieveView(
    generics.RetrieveAPIView
):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []


class OfferListCreateView(generics.ListCreateAPIView):
    pagination_class = OfferPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = OfferFilter

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "updated_at",
        "min_price",
    ]

    ordering = [
        "-updated_at",
    ]

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
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferWriteSerializer

        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []


class OfferRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [
        IsAuthenticated,
        IsOfferOwnerOrReadOnly,
    ]

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
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferDetailViewSerializer

        return OfferWriteSerializer