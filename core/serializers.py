from rest_framework import serializers

from core.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [
            "card_id",
            "name",
            "number",
            "month",
            "year",
            "cvv",
            "amount",
            "card_type",
            "date",
        ]
        read_only_fields = ["card_id", "amount", "date"]




class FundCreditCardSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )

