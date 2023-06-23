from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import MyTokenObtainPairView, UserRegisterView, UserRetrieveView, TaskViewSet, RewardViewSet

app_name = "core"

router = DefaultRouter()

router.register("tasks", TaskViewSet)
router.register("rewards", RewardViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/register/", UserRegisterView.as_view(), name="user_register"),
    path("users/<int:pk>/", UserRetrieveView.as_view(), name="user_retrieve_update")
]
