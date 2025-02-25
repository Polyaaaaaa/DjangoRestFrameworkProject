from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.filters import PaymentsFilter
from users.models import Payments
from users.serializers import PaymentsSerializers


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