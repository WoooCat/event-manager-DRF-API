from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer


@extend_schema(auth=[])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)


@extend_schema(auth=[])
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(auth=[])
class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenRefreshSerializer