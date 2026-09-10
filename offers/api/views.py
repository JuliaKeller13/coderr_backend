from rest_framework import generics

from offers.models import Offer

from .pagination import OfferPagination
from .permissions import IsBusinessUser
from .serializers import OfferSerializer


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []