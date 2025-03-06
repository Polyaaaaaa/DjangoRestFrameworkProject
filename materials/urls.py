from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView
from users.views import PaymentsCreateAPIView, PaymentsListAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, UserDestroyAPIView, RegisterAPIView
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

                  # Payments
                  path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments_create'),
                  path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),

                  path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                  path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

                  # Users
                  path('users/', UserListAPIView.as_view(), name='user_list'),
                  path('users/register/', RegisterAPIView.as_view(), name='user-register'),
                  path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
                  path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
                  path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),

                  path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),

              ] + router.urls
