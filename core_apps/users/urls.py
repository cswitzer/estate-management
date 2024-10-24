from django.urls import path, re_path

from .views import (
    CustomProviderAuthView,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
    LogoutAPIView,
)

urlpatterns = [
    # /o/google/
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("refresh/", CustomTokenRefreshView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
]
