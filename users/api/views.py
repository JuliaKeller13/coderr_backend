from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile

from .permissions import IsProfileOwnerOrReadOnly
from .serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)


def create_auth_response(user, status_code):
    token, _ = Token.objects.get_or_create(user=user)
    data = {
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
    }
    return Response(data, status=status_code)


class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return create_auth_response(
            user,
            status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return create_auth_response(
            user,
            status.HTTP_200_OK,
        )


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
        IsProfileOwnerOrReadOnly,
    ]
    queryset = Profile.objects.select_related("user")
    lookup_field = "user_id"
    lookup_url_kwarg = "pk"


class BusinessProfileListView(generics.ListAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(
        type=Profile.UserType.BUSINESS
    ).select_related("user")


class CustomerProfileListView(generics.ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(
        type=Profile.UserType.CUSTOMER
    ).select_related("user")
