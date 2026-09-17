from django.db.models import Avg

from rest_framework.response import Response
from rest_framework.views import APIView

from offers.models import Offer
from reviews.models import Review
from users.models import Profile


class BaseInfoView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        review_count = Review.objects.count()

        average_rating = Review.objects.aggregate(
            average=Avg("rating")
        )["average"]

        business_profile_count = Profile.objects.filter(
            type=Profile.UserType.BUSINESS
        ).count()

        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": (
                    round(average_rating, 1)
                    if average_rating is not None
                    else 0.0
                ),
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )