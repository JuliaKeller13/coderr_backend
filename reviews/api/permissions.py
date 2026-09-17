from rest_framework.permissions import BasePermission

from users.models import Profile


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.profile.type
            == Profile.UserType.CUSTOMER
        )


class IsReviewOwner(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return obj.reviewer == request.user