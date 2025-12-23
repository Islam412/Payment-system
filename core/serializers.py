from rest_framework import serializers

from core.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [ '__all__' ]
        read_only_fields = ["card_id", "amount", "date"]
