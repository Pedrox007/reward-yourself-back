from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from core.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom Access token View
    """
    serializer_class = MyTokenObtainPairSerializer
