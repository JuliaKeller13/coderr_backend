from rest_framework import status

from reviews.models import Review

from .base import ReviewAPITestBase


class ReviewListTests(ReviewAPITestBase):

    def create_review(
        self,
        reviewer=None,
        business=None,
        rating=4,
        description="Sehr guter Service.",
    ):
        return Review.objects.create(
            reviewer=reviewer or self.customer_user,
            business_user=business or self.business_user,
            rating=rating,
            description=description,
        )

    def test_authenticated_user_can_list_reviews(self):
        self.create_review()

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/reviews/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_unauthenticated_user_cannot_list_reviews(self):
        response = self.client.get(
            "/api/reviews/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_filter_by_business_user_id(self):
        other_business = self.create_business_user()

        own_review = self.create_review()

        self.create_review(
            business=other_business,
            description="Other business",
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            (
                "/api/reviews/"
                f"?business_user_id={self.business_user.id}"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            own_review.id,
        )

    def test_filter_by_reviewer_id(self):
        other_customer = self.create_customer_user()

        own_review = self.create_review()

        self.create_review(
            reviewer=other_customer,
            description="Other reviewer",
        )

        self.client.force_authenticate(
            user=self.business_user
        )

        response = self.client.get(
            (
                "/api/reviews/"
                f"?reviewer_id={self.customer_user.id}"
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            own_review.id,
        )

    def test_ordering_by_rating(self):
        self.create_review(
            rating=5,
            description="Five stars",
        )

        other_business = self.create_business_user()

        self.create_review(
            business=other_business,
            rating=2,
            description="Two stars",
        )

        self.client.force_authenticate(
            user=self.customer_user
        )

        response = self.client.get(
            "/api/reviews/?ordering=rating"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["rating"],
            2,
        )

        self.assertEqual(
            response.data[1]["rating"],
            5,
        )