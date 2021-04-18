from rest_framework import generics
from user.serializers import UserSerializer, AuthTokeSerialzier
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new token for user"""
    serializer_class = AuthTokeSerialzier
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
