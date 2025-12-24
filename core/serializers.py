from rest_framework import serializers

from core.models import CreditCard , Transaction , Home
from account.models import Account


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



# transaction api
class TransactionSerializer(serializers.ModelSerializer):
    sender_full_name = serializers.SerializerMethodField()
    receiver_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "amount",
            "description",
            "status",
            "transaction_type",
            "sender",
            "receiver",
            "sender_account",
            "reciever_account",
            "date",
            "updated",
            "sender_full_name",
            "receiver_full_name"
        ]

    def get_sender_full_name(self, obj):
        try:
            return obj.sender.kyc.full_name
        except:
            return None

    def get_receiver_full_name(self, obj):
        try:
            return obj.reciever.kyc.full_name
        except:
            return None



# transfer api
class AccountSearchSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['account_id', 'account_number', 'user', 'user_full_name']

    def get_user_full_name(self, obj):
        try:
            return obj.user.kyc.full_name
        except:
            return obj.user.username



class AccountDetailSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['account_id', 'account_number', 'user', 'user_full_name']

    def get_user_full_name(self, obj):
        try:
            return obj.user.kyc.full_name
        except:
            return obj.user.username



class AmountTransferProcessSerializer(serializers.Serializer):
    amount_send = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=1000, allow_blank=True, required=False)



class TransferFinalProcessSerializer(serializers.Serializer):
    pin_number = serializers.CharField(max_length=10)



# home api
class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = [
            "image",
            "supported_currencies",
            "available_countries",
            "payment_methods",
            "support_team_day",
            "support_team_hour",
            "peace_of_mind",
            "business_ready",
            "transparent",
            "international_network",
            "payments",
            "collections",
            "conversions",
            "global_account",
            "register_for_free",
            "set_up_your_transfer",
            "make_your_payment",
            "you_all_done",
        ]
