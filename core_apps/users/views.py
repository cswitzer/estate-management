import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView  # for google
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)  # for obtaining and refreshing tokens

logger = logging.getLogger(__name__)


def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    """
    When we get tokens from the response, we set them as httpOnly cookies and send them back to the client.
    """
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }
    response.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Get the tokens from the response and set them as cookies.
        After that, remove them from the response data so they are not exposed to the client.

        Honestly, this view is basically the same as the TokenObtainPairView, but we are just adding
        the additional step of setting the tokens as cookies.
        """
        token_res = super().post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(token_res, access_token, refresh_token)

                # We do not want these tokens here because they are already set as cookies.
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)

                token_res.data["message"] = "Login Successful."
            else:
                token_res.data["message"] = "Login Failed."
                logger.error(
                    "Access or refresh token not found in login response data."
                )

        return token_res


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Get the tokens from the response and set them as cookies.
        After that, remove them from the response data so they are not exposed to the client.
        """
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        # This line will refresh the token, but will not set the cookies.
        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            refresh_token = refresh_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(refresh_res, access_token, refresh_token)

                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = "Access token refreshed successfully."
            else:
                refresh_res.data["message"] = (
                    "Access or refresh tokens not found in refresh response data."
                )
                logger.error(
                    "Access of refresh token not found in login response data."
                )

        return refresh_res


class CustomProviderAuthView(ProviderAuthView):
    """
    Used for social authentication with cookies using Google.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Get the tokens from the response and set them as cookies.
        After that, remove them from the response data so they are not exposed to the client.
        """
        provider_res = super().post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(provider_res, access_token, refresh_token)

                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                provider_res.data["message"] = "You are logged in successfully."
            else:
                provider_res.data["message"] = (
                    "Access or refresh token not found in the provider response."
                )
                logger.error(
                    "Access or refresh token not found in the provider response data."
                )

        return provider_res


class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
