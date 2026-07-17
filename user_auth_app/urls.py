
from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(),
         name='register'),
    path('login/', CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', CookieLogoutView.as_view(),
         name='logout'),
]
