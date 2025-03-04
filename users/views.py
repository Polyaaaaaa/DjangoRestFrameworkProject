from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from materials.permissions import IsOwnerOrStaff
from users.filters import PaymentsFilter
from users.models import Payments, User
from users.serializers import PaymentsSerializers, UserSerializer


# Create your views here.
class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializers


class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentsFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # По умолчанию сортировка от новых к старым


class RegisterAPIView(generics.CreateAPIView):
    """Создание нового пользователя (регистрация)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """Получение списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsOwnerOrStaff] # Доступ для владельцев или модераторов


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Получение одного пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrStaff]  # Только владелец или админ


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrStaff]  # Только владелец или админ


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrStaff]  # Только владелец или админ
