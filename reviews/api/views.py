from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review

from .filters import ReviewFilter
from .permissions import (
    IsCustomerUser,
    IsReviewOwner,
)
from .serializers import (
    ReviewSerializer,
    ReviewUpdateSerializer,
)


class ReviewListCreateView(
    generics.ListCreateAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = ReviewFilter

    ordering_fields = [
        "updated_at",
        "rating",
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerUser()]

        return [IsAuthenticated()]


class ReviewDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer

    permission_classes = [
        IsAuthenticated,
        IsReviewOwner,
    ]

    http_method_names = [
        "patch",
        "delete",
        "options",
    ]