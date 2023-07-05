from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from core.models import User, Task, Reward


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
                    "access": str(refresh.access_token),
                    "name": str(self.user.first_name),
                    "id": str(self.user.id)
                }

                update_last_login(None, self.user)

                return data

            else:
                raise exceptions.AuthenticationFailed(
                    detail="Wrong password")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()), User.username_validator]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class TaskSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())

    class Meta:
        model = Task
        exclude = ("user",)


class RewardSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())

    class Meta:
        model = Reward
        exclude = ("user",)
