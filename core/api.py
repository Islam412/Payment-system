from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models import CreditCard
from account.models import Account
from .serializers import CreditCardSerializer


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
