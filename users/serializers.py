from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
        )


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
