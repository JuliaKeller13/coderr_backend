from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
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


class RegistrationView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
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