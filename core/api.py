from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .serializers import CreditCardSerializer , FundCreditCardSerializer
from core.models import CreditCard , Notification
from account.models import Account


class CreditCardDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, card_id):
        try:
            credit_card = CreditCard.objects.get(
                card_id=card_id,
                user=request.user
            )
        except CreditCard.DoesNotExist:
            return Response(
                {"detail": "Credit card not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        account = Account.objects.get(user=request.user)

        serializer = CreditCardSerializer(credit_card)

        return Response({
            "account_balance": account.account_balance,
            "credit_card": serializer.data
        }, status=status.HTTP_200_OK)




class FundCreditCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_id):
        serializer = FundCreditCardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid amount."},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = serializer.validated_data["amount"]

        try:
            credit_card = CreditCard.objects.get(
                card_id=card_id,
                user=request.user
            )
        except CreditCard.DoesNotExist:
            return Response(
                {"detail": "Credit card not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        account = Account.objects.get(user=request.user)

        if amount > account.account_balance:
            return Response(
                {"detail": "Insufficient funds."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update balances
        account.account_balance -= amount
        account.save()

        credit_card.amount += amount
        credit_card.save()

        # Optional notification
        Notification.objects.create(
            user=request.user,
            notification_type="Funded Credit Card",
            amount=amount
        )

        return Response(
            {
                "message": "Credit card funded successfully.",
                "card_balance": credit_card.amount,
                "account_balance": account.account_balance
            },
            status=status.HTTP_200_OK
        )
