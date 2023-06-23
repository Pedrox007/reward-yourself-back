from django.shortcuts import render
from rest_framework import mixins, viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import User, Task, Reward
from core.permissions import IsOwnerOrSuperUser
from core.serializers import MyTokenObtainPairSerializer, UserSerializer, TaskSerializer, RewardSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom Access token View
    """
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)
    filterset_fields = ["finished", "fixed"]
    search_fields = ["title", "description"]
    ordering_fields = ["finished", "fixed", "coin_reward"]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset

    @action(detail=True, methods=["patch"], url_path="finish", name="finish-task")
    def finish(self, request, pk=None):
        task = self.get_object()
        user = task.user

        if not task.fixed:
            task.finished = True
            task.save()

        user.coins += task.coin_reward
        user.save()

        return Response(data=TaskSerializer(task).data, status=status.HTTP_200_OK)


class RewardViewSet(ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)
    filterset_fields = ["cost", "duration"]
    search_fields = ["title", "description"]
    ordering_fields = ["cost", "duration"]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset

    @action(detail=True, methods=["patch"], url_path="buy", name="buy-reward")
    def buy(self, request, pk=None):
        reward = self.get_object()
        user = reward.user

        response_message = {"message": "success"}
        response_status = status.HTTP_200_OK

        if reward.cost > user.coins:
            response_message["message"] = "User don't have sufficient coins."
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            user.coins -= reward.cost
            user.save()

        return Response(data=response_message, status=response_status)
