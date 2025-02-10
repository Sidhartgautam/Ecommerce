from django.urls import path
from .views import GoogleAuthView,LoginUserView,RegisterUserView

urlpatterns = [
    path('auth/google/', GoogleAuthView.as_view(), name='google_login'),
    path('auth/login/', LoginUserView.as_view(), name='login_user'),
    path('auth/register/', RegisterUserView.as_view(), name='register_user'),
]
