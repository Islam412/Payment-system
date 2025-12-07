from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Account, KYC
from .serializers import AccountSerializer, KYCSerializer


class AccountDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(account)
        return Response(serializer.data)



