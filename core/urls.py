from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import MyTokenObtainPairView, UserRegisterView, UserRetrieveView

app_name = "core"

# router = DefaultRouter()

# router.register("user", UserViewSet)

urlpatterns = [
    # path("", include(router.urls())),
    path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path("user/register/", UserRegisterView.as_view(), name="user_register"),
    path("user/<int:pk>/", UserRetrieveView.as_view(), name="user_retrieve_update")
]
