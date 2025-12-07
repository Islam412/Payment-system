from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# genric based views api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView
)



from .models import Account, KYC
from core.models import CreditCard

from .serializers import AccountSerializer, KYCSerializer, CreditCardSerializer




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def account_api(request):
    account = Account.objects.get(user=request.user)
    
    serializer = AccountSerializer(account)
    return Response(serializer.data)



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def kyc_api(request):
    user = request.user

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == "POST":
        serializer = KYCSerializer(kyc, data=request.data, partial=True)
        if serializer.is_valid():
            obj = serializer.save(user=user, account=user.account)
            return Response({
                "message": "KYC submitted successfully.",
                "data": KYCSerializer(obj).data
            })
        return Response(serializer.errors, status=400)

    # GET
    if kyc:
        return Response(KYCSerializer(kyc).data)
    else:
        return Response({"message": "No KYC found"}, status=404)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    user = request.user

    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    credit_cards = CreditCard.objects.filter(user=user)

    return Response({
        "account": AccountSerializer(account).data,
        "kyc": KYCSerializer(kyc).data if kyc else None,
        "credit_cards": CreditCardSerializer(credit_cards, many=True).data,
    })



# --------- genric based views api ----------------
class AccountView(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Account.objects.get(user=self.request.user)



