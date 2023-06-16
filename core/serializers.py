from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from core.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    user: User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del self.fields[self.username_field]
        self.fields["login"] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        password = attrs.get("password")
        login = attrs.get("login")

        if "@" in login:
            self.user = User.objects.filter(email__iexact=login).first()
        else:
            self.user = User.objects.filter(username__iexact=login).first()

        if self.user is None:
            raise exceptions.AuthenticationFailed(detail="Credentials does not exist!")
        else:
            if self.user.check_password(password):
                refresh = self.get_token(self.user)

                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }

                update_last_login(None, self.user)

                return data

            else:
                raise exceptions.AuthenticationFailed(
                    detail="Wrong password")
