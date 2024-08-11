from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.tokens import AccessToken

class CustomUserAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

class CustomJWTAuthentication(JWTAuthentication):   
    def get_raw_token(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return None
            return token
        except ValueError:
            # If the Authorization header is not in the expected format
            return None

    def authenticate(self, request):
        # Extract JWT token from the request headers
        raw_token = self.get_raw_token(request)
        if not raw_token:
            return None

        # Decode the access token to extract the user ID
        try:
            decoded_token = AccessToken(raw_token)
            user_id = decoded_token.payload.get('user_id')
            print("User ID:", user_id)

            # Return the user object directly using the extracted user ID
            # You can customize this part to fetch the user from your database
            user = CustomUser.objects.get(id=user_id)
            return (user, raw_token)  # Return the user object and the raw token
        except Exception as e:
            # Handle token decoding errors
            print(f"Error decoding access token: {e}")
            return None