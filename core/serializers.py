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
