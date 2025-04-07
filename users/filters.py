import django_filters
from users.models import Payments


class PaymentsFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(
        field_name="paid_course", lookup_expr="exact"
    )
    paid_lesson = django_filters.NumberFilter(
        field_name="paid_lesson", lookup_expr="exact"
    )
    payment_method = django_filters.ChoiceFilter(choices=Payments.PAYMENT_METHODS)
    payment_date = django_filters.OrderingFilter(fields=("payment_date",))

    class Meta:
        model = Payments
        fields = ["paid_course", "paid_lesson", "payment_method", "payment_date"]
