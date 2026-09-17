from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers.models import Offer
from reviews.models import Review
from users.models import Profile


class BaseInfoView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "review_count": Review.objects.count(),
            "average_rating": self._get_average_rating(),
            "business_profile_count": self._get_business_profile_count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)

    @staticmethod
    def _get_average_rating():
        average = Review.objects.aggregate(
            average=Avg("rating")
        )["average"]
        return round(average, 1) if average is not None else 0.0

    @staticmethod
    def _get_business_profile_count():
        return Profile.objects.filter(
            type=Profile.UserType.BUSINESS
        ).count()
