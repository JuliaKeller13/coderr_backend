from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review

from .permissions import IsCustomerUser
from .serializers import ReviewSerializer


class ReviewListCreateView(
    generics.ListCreateAPIView
):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerUser()]

        return [IsAuthenticated()]