# from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from materials.permissions import IsOwnerOrStaff
from users.filters import PaymentsFilter
from users.models import Payments, User
from users.serializers import PaymentsSerializers, UserSerializer
from users.services import convert_currencies, create_price, create_session


# Create your views here.
class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_currencies(payment.amount)
        price = create_price(amount_in_dollars)
        session_id, payment_link = create_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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
    permission_classes = [
        IsAuthenticated & IsOwnerOrStaff
    ]  # Доступ для владельцев или модераторов


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
