from rest_framework import serializers

from core.models import CreditCard


# credit card
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





class WithdrawCreditCardSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )




# payment requist
class AmountRequestProcessSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )
    description = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True
    )




class AmountRequestFinalSerializer(serializers.Serializer):
    pin_number = serializers.CharField(max_length=10)



class SettlementProcessSerializer(serializers.Serializer):
    pin_number = serializers.CharField(max_length=10)