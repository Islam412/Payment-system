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





class KYCSubmitAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return KYC details if exists"""
        try:
            kyc = KYC.objects.get(user=request.user)
            serializer = KYCSerializer(kyc)
            return Response(serializer.data)
        except KYC.DoesNotExist:
            return Response({"detail": "KYC not submitted yet"}, status=404)

    def post(self, request):
        """Submit or update KYC form"""
        user = request.user
        account = Account.objects.get(user=user)

        try:
            kyc = KYC.objects.get(user=user)
            serializer = KYCSerializer(kyc, data=request.data, partial=True)
        except KYC.DoesNotExist:
            serializer = KYCSerializer(data=request.data)

        if serializer.is_valid():
            kyc_obj = serializer.save(user=user, account=account)
            return Response({
                "message": "KYC Submitted Successfully",
                "data": KYCSerializer(kyc_obj).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
