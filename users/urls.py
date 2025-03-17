from django.urls import path
from drf_yasg import openapi

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import (
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    RegisterAPIView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view

app_name = UsersConfig.name

router = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Payments
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/register/", RegisterAPIView.as_view(), name="user-register"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
] + router.urls
