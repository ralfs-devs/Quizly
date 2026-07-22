from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_auth_app.api.serializers import RegistrationSerializer
from user_auth_app.utils import ManageTokenCookies


class RegistrationView(APIView):
    """Handles user registration."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    """Handles login and sets authentication cookies."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Den User aus der Validierung des Serializers extrahieren
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.user

        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

        return ManageTokenCookies.create_response(
            response.data,
            "Login successfull",
            user=user_info
        )


class CookieTokenRefreshView(TokenRefreshView):
    """Refreshes authentication tokens using cookies."""

    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh_token')

        try:
            response = super().post(request, *args, **kwargs)
            return ManageTokenCookies.create_response(response.data, "Token refreshed")
        except Exception:
            return Response(
                {"detail": "Session expired: Refresh token invalid oder missing."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CookieLogoutView(APIView):
    """Handles user logout by deleting authentication cookies."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout_message = "Logout successfull! All Tokens deleted. Refresh token is invalid"
        return ManageTokenCookies.clear_cookies(logout_message)
