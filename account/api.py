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
class AccountViewAPI(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(account, context={"request": request})
        return Response(serializer.data)



class KYCViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            kyc = KYC.objects.get(user=request.user)
            serializer = KYCSerializer(kyc, context={"request": request})
            return Response(serializer.data)
        except KYC.DoesNotExist:
            return Response({"message": "No KYC found"}, status=404)

    def post(self, request):
        try:
            kyc = KYC.objects.get(user=request.user)
            serializer = KYCSerializer(
                kyc,
                data=request.data,
                partial=True,
                context={"request": request},
            )
        except KYC.DoesNotExist:
            serializer = KYCSerializer(
                data=request.data,
                context={"request": request},
            )

        if serializer.is_valid():
            saved_obj = serializer.save(
                user=request.user,
                account=request.user.account
            )

            return Response({
                "message": "KYC submitted successfully.",
                "data": KYCSerializer(saved_obj, context={"request": request}).data
            })

        return Response(serializer.errors, status=400)




class DashboardViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        account = Account.objects.get(user=user)

        try:
            kyc = KYC.objects.get(user=user)
        except KYC.DoesNotExist:
            kyc = None

        credit_cards = CreditCard.objects.filter(user=user)

        return Response({
            "account": AccountSerializer(account, context={"request": request}).data,
            "kyc": KYCSerializer(kyc, context={"request": request}).data if kyc else None,
            "credit_cards": CreditCardSerializer(credit_cards, many=True, context={"request": request}).data
        })




class AddCardViewAPI(CreateAPIView):
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delete_account_api(request):
    user = request.user
    if request.method == "GET":
        cards = CreditCard.objects.filter(user=user).values(
            "id", "card_id", "amount"
        )

        return Response(
            {
                "success": True,
                "cards": cards,
                "message": "Select a card to transfer your balance before deleting account"
            },
            status=status.HTTP_200_OK
        )
    serializer = DeleteAccountSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    card_id = serializer.validated_data["card_id"]

    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        return Response(
            {"success": False, "message": "Account not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        card = CreditCard.objects.get(id=card_id, user=user)
    except CreditCard.DoesNotExist:
        return Response(
            {"success": False, "message": "Invalid card selection"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        balance = account.account_balance

        card.amount += balance
        card.save()

        user.delete()

    return Response(
        {
            "success": True,
            "message": f"Balance {balance} transferred to card ending with {card.card_id}. Account deleted successfully."
        },
        status=status.HTTP_200_OK
    )
