from rest_framework import serializers
from .models import Account, KYC
from core.models import CreditCard

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class KYCSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    identity_image_url = serializers.SerializerMethodField()
    signature_url = serializers.SerializerMethodField()
    class Meta:
        model = KYC
        fields = "__all__"
        read_only_fields = ['user', 'account']

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_identity_image_url(self, obj):
        request = self.context.get("request")
        if obj.identity_image:
            return request.build_absolute_uri(obj.identity_image.url)
        return None

    def get_signature_url(self, obj):
        request = self.context.get("request")
        if obj.signature:
            return request.build_absolute_uri(obj.signature.url)
        return None
    


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"
        read_only_fields = ['user']
