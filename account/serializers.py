from rest_framework import serializers
from .models import Account, KYC




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ("id", "user", "account_number", "account_id", "pin_number", "red_code", "date")



class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = "__all__"
        read_only_fields = ("id", "user", "account", "date")
