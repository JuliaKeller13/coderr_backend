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

class IsOrderBusinessUser(BasePermission):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        if not request.user.is_authenticated:
            return False

        if (
            request.user.profile.type
            != Profile.UserType.BUSINESS
        ):
            return False

        return obj.business_user == request.user