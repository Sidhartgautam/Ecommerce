from django.urls import path
from .views import GoogleAuthView,LoginUserView,RegisterUserView,UserProfileView,HomeView

urlpatterns = [
    path('auth/google/', GoogleAuthView.as_view(), name='google_login'),
    path('auth/login/', LoginUserView.as_view(), name='login_user'),
    path('auth/register/', RegisterUserView.as_view(), name='register_user'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('home/', HomeView.as_view(), name='home'),
]
