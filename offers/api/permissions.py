from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from users.models import Profile


class IsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.profile.type
            == Profile.UserType.BUSINESS
        )


class IsOfferOwnerOrReadOnly(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user