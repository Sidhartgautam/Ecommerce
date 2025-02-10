from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer
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
            # Hash the password before saving the user
            serializer.save(password=make_password(data.get('password')))
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
