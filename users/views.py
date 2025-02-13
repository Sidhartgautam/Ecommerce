from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer, UserProfileSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required."}, status=400)

        try:
            # Verify the Google OAuth token
            id_info = id_token.verify_oauth2_token(
                token, google_requests.Request(), settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
            )

            # Extract user details from the token
            email = id_info.get('email')
            first_name = id_info.get('given_name')
            last_name = id_info.get('family_name')

            # Check if the user exists or create a new user
            user, created = CustomUser.objects.get_or_create(
                email=email, defaults={
                    'username': email.split('@')[0], 
                    'first_name': first_name, 
                    'last_name': last_name
                })

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Google login successful",
                "is_new_user": created
            }, status=200)

        except ValueError:
            return Response({"error": "Invalid token."}, status=400)
        
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User registered successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            user = CustomUser.objects.filter(email=username).first()
            if user:
                user = authenticate(username=user.username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful"
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ Fetch logged-in user's profile """
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({"success": True, "user": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """ Update logged-in user's profile (except email & username) """
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Profile updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
