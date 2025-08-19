from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, MyTokenRefreshView


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/jwt/create/", MyTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", MyTokenRefreshView.as_view(), name="jwt-refresh"),
]
