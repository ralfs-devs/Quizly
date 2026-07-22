from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class ManageTokenCookies:
    """Utility class to centralize cookie and response management."""

    @staticmethod
    def create_response(data, detail, status_code=200, user=None):
        """Creates a response with tokens in cookies and consistent JSON body."""
        response = Response({"detail": detail}, status=status_code)

        if "access" in data:
            response.set_cookie(
                "access_token",
                data["access"],
                httponly=True,
                samesite="Lax",
                path="/"
            )
        if "refresh" in data:
            response.set_cookie(
                "refresh_token",
                data["refresh"],
                httponly=True,
                samesite="Lax",
                path="/"
            )
        if user:
            response.data["user"] = user

        return response

    @staticmethod
    def clear_cookies(detail):
        """Clears auth cookies and returns a simple response."""
        response = Response({"detail": detail})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class JWTCookieAuthentication(JWTAuthentication):
    """Custom authentication class to extract JWT tokens from cookies."""

    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None

        if header is None:
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
