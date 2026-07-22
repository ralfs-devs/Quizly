
from django.urls import path
from user_auth_app.api.views import (
    RegistrationView,
    CookieTokenObtainPairView,
    CookieLogoutView,
    CookieTokenRefreshView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(),
         name='register'),
    path('login/', CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('logout/', CookieLogoutView.as_view(),
         name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(),
         name='token_refresh'),
]
