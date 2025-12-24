from django.db.models import Q
from django.db import transaction as db_transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import Decimal , InvalidOperation

from .serializers import CreditCardSerializer , FundCreditCardSerializer , WithdrawCreditCardSerializer , AmountRequestProcessSerializer , AmountRequestFinalSerializer , SettlementProcessSerializer , TransactionSerializer , AccountSearchSerializer , AccountDetailSerializer , AmountTransferProcessSerializer , TransferFinalProcessSerializer
from core.models import CreditCard , Notification , Transaction
from account.models import Account
from userauths.models import User



# credit card
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




class WithdrawCreditCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, card_id):
        serializer = WithdrawCreditCardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": "Please enter a valid amount greater than zero."},
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

        if credit_card.amount < amount:
            return Response(
                {"detail": "Insufficient funds."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update balances
        credit_card.amount -= amount
        credit_card.save()

        account.account_balance += amount
        account.save()

        # Notification
        Notification.objects.create(
            user=request.user,
            amount=amount,
            notification_type="Withdrew Credit Card Funds"
        )

        return Response(
            {
                "message": "Withdrawal successful.",
                "card_balance": credit_card.amount,
                "account_balance": account.account_balance
            },
            status=status.HTTP_200_OK
        )



class DeleteCreditCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, card_id):
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

        # Return remaining balance to account
        if credit_card.amount > 0:
            account.account_balance += credit_card.amount
            account.save()

        # Notification
        Notification.objects.create(
            user=request.user,
            notification_type="Deleted Credit Card"
        )

        credit_card.delete()

        return Response(
            {"message": "Credit card deleted successfully."},
            status=status.HTTP_200_OK
        )




# payment requist
class SearchUsersRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get("account_number")
        accounts = Account.objects.all()

        if query:
            accounts = accounts.filter(
                Q(account_number=query) |
                Q(account_id=query)
            ).distinct()

        # Serialize minimal info
        results = [
            {
                "account_id": acc.account_id,
                "account_number": acc.account_number,
                "user_id": acc.user.id,
                "full_name": getattr(acc.user.kyc, "full_name", acc.user.username)
            }
            for acc in accounts
        ]

        return Response(
            {
                "query": query,
                "results": results
            },
            status=status.HTTP_200_OK
        )



class AmountRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "account": {
                    "account_id": account.account_id,
                    "account_number": account.account_number,
                    "user_id": account.user.id,
                    "full_name": getattr(
                        account.user.kyc,
                        "full_name",
                        account.user.username
                    )
                }
            },
            status=status.HTTP_200_OK
        )




class AmountRequestProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number):
        serializer = AmountRequestProcessSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reciever_account = Account.objects.get(
                account_number=account_number
            )
        except Account.DoesNotExist:
            return Response(
                {"detail": "Receiver account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        sender = request.user
        reciever = reciever_account.user

        if sender == reciever:
            return Response(
                {"detail": "You cannot request money from yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = Transaction.objects.create(
            user=sender,
            amount=serializer.validated_data["amount"],
            description=serializer.validated_data.get("description", ""),

            sender=sender,
            reciever=reciever,

            sender_account=sender.account,
            reciever_account=reciever_account,

            status="request_sent",
            transaction_type="request",
        )

        return Response(
            {
                "message": "Payment request sent successfully.",
                "transaction_id": transaction.transaction_id,
                "receiver_account_number": reciever_account.account_number
            },
            status=status.HTTP_201_CREATED
        )





class AmountRequestConfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(
                account_number=account_number
            )
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(
                transaction_id=transaction_id
            )
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "account": {
                    "account_id": account.account_id,
                    "account_number": account.account_number,
                    "user_id": account.user.id,
                    "full_name": getattr(
                        account.user.kyc,
                        "full_name",
                        account.user.username
                    )
                },
                "transaction": {
                    "transaction_id": transaction.transaction_id,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "status": transaction.status,
                    "transaction_type": transaction.transaction_type,
                    "sender": transaction.sender.id if transaction.sender else None,
                    "receiver": transaction.reciever.id if transaction.reciever else None,
                    "date": transaction.date
                }
            },
            status=status.HTTP_200_OK
        )




class AmountRequestFinalProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number, transaction_id):
        serializer = AmountRequestFinalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        pin_number = serializer.validated_data["pin_number"]

        if pin_number != request.user.account.pin_number:
            return Response(
                {"detail": "Invalid PIN number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction.status = "request_sent"
        transaction.save()

        Notification.objects.create(
            user=account.user,
            notification_type="Recieved Payment Request",
            amount=transaction.amount,
        )

        Notification.objects.create(
            user=request.user,
            notification_type="Sent Payment Request",
            amount=transaction.amount,
        )

        return Response(
            {
                "message": "Payment request sent successfully.",
                "transaction_id": transaction.transaction_id
            },
            status=status.HTTP_200_OK
        )




class AmountRequestCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "account": {
                    "account_id": account.account_id,
                    "account_number": account.account_number,
                    "user_id": account.user.id,
                    "full_name": getattr(
                        account.user.kyc,
                        "full_name",
                        account.user.username
                    )
                },
                "transaction": {
                    "transaction_id": transaction.transaction_id,
                    "amount": transaction.amount,
                    "status": transaction.status,
                    "transaction_type": transaction.transaction_type,
                    "description": transaction.description,
                    "sender": transaction.sender.id if transaction.sender else None,
                    "receiver": transaction.reciever.id if transaction.reciever else None,
                    "date": transaction.date
                }
            },
            status=status.HTTP_200_OK
        )



# >>>>>>>>>>>>>>>Settled API<<<<<<<<<<<<<<<<<<<< #
class SettlementConfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "account": {
                    "account_id": account.account_id,
                    "account_number": account.account_number,
                    "user_id": account.user.id,
                    "full_name": getattr(
                        account.user.kyc,
                        "full_name",
                        account.user.username
                    )
                },
                "transaction": {
                    "transaction_id": transaction.transaction_id,
                    "amount": transaction.amount,
                    "status": transaction.status,
                    "transaction_type": transaction.transaction_type,
                    "description": transaction.description,
                    "sender": transaction.sender.id if transaction.sender else None,
                    "receiver": transaction.reciever.id if transaction.reciever else None,
                    "date": transaction.date
                }
            },
            status=status.HTTP_200_OK
        )





class SettlementProcessingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number, transaction_id):
        serializer = SettlementProcessSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receiver_account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Receiver account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        sender_account = request.user.account
        pin_number = serializer.validated_data["pin_number"]

        if pin_number != sender_account.pin_number:
            return Response(
                {"detail": "Incorrect PIN."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sender_account.account_balance < transaction.amount:
            return Response(
                {"detail": "Insufficient funds."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with db_transaction.atomic():
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            receiver_account.account_balance += transaction.amount
            receiver_account.save()

            transaction.status = "request_settled"
            transaction.save()

        return Response(
            {
                "message": "Settlement completed successfully.",
                "transaction_id": transaction.transaction_id,
                "amount": transaction.amount,
                "sender_balance": sender_account.account_balance,
                "receiver_balance": receiver_account.account_balance,
            },
            status=status.HTTP_200_OK
        )




class SettlementCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "account": {
                    "account_id": account.account_id,
                    "account_number": account.account_number,
                    "user_id": account.user.id,
                    "full_name": getattr(
                        account.user.kyc,
                        "full_name",
                        account.user.username
                    )
                },
                "transaction": {
                    "transaction_id": transaction.transaction_id,
                    "amount": transaction.amount,
                    "status": transaction.status,
                    "transaction_type": transaction.transaction_type,
                    "description": transaction.description,
                    "sender": transaction.sender.id if transaction.sender else None,
                    "receiver": transaction.reciever.id if transaction.reciever else None,
                    "date": transaction.date
                }
            },
            status=status.HTTP_200_OK
        )




class DeletePaymentRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔐 Check if the requester is the creator of the payment request
        if request.user != transaction.user:
            return Response(
                {"detail": "You are not authorized to delete this request."},
                status=status.HTTP_403_FORBIDDEN
            )

        transaction.delete()
        return Response(
            {"message": "Payment request deleted successfully."},
            status=status.HTTP_200_OK
        )



# transaction api
class TransactionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender_transfer = Transaction.objects.filter(sender=request.user, transaction_type='Transfer').order_by('-id')
        receiver_transfer = Transaction.objects.filter(reciever=request.user, transaction_type='Transfer').order_by('-id')

        request_sender = Transaction.objects.filter(sender=request.user, transaction_type='request').order_by('-id')
        request_receiver = Transaction.objects.filter(reciever=request.user, transaction_type='request').order_by('-id')

        return Response({
            "transfer": {
                "sent": TransactionSerializer(sender_transfer, many=True).data,
                "received": TransactionSerializer(receiver_transfer, many=True).data
            },
            "request": {
                "sent": TransactionSerializer(request_sender, many=True).data,
                "received": TransactionSerializer(request_receiver, many=True).data
            }
        })



class TransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in [transaction.sender, transaction.reciever]:
            return Response(
                {"detail": "Unauthorized access."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# transfer api
class SearchUsersAccountNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get("account_number")
        accounts = Account.objects.all()

        if query:
            accounts = accounts.filter(
                Q(account_number=query) | Q(account_id=query)
            ).distinct()

        serializer = AccountSearchSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class AmountTransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AmountTransferProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number):
        serializer = AmountTransferProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver_account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            return Response({"detail": "Receiver account not found."}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        receiver = receiver_account.user
        sender_account = sender.account
        amount = serializer.validated_data["amount_send"]
        description = serializer.validated_data.get("description", "")

        if sender_account.account_balance < amount:
            return Response({"detail": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction
        transaction = Transaction.objects.create(
            user=sender,
            amount=amount,
            description=description,
            reciever=receiver,
            sender=sender,
            sender_account=sender_account,
            reciever_account=receiver_account,
            status="processing",
            transaction_type="Transfer"
        )

        return Response(
            {
                "message": "Transaction created successfully.",
                "transaction_id": transaction.transaction_id,
                "amount": transaction.amount,
                "sender_balance": sender_account.account_balance,
            },
            status=status.HTTP_201_CREATED
        )




class TransferConfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Account.DoesNotExist:
            return Response({"detail": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in [transaction.sender, transaction.reciever]:
            return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TransactionSerializer(transaction)
        return Response({
            "account": {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "user_id": account.user.id,
                "full_name": getattr(account.user.kyc, "full_name", account.user.username)
            },
            "transaction": serializer.data
        }, status=status.HTTP_200_OK)




class TransferFinalProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number, transaction_id):
        serializer = TransferFinalProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver_account = Account.objects.get(account_number=account_number)
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Account.DoesNotExist:
            return Response({"detail": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction does not exist."}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        sender_account = sender.account
        receiver = receiver_account.user
        amount = transaction.amount
        pin_number = serializer.validated_data['pin_number']

        if pin_number != sender_account.pin_number:
            return Response({"detail": "Incorrect PIN."}, status=status.HTTP_403_FORBIDDEN)

        if sender_account.account_balance < amount:
            return Response({"detail": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        sender_account.account_balance -= amount
        sender_account.save()

        receiver_account.account_balance += amount
        receiver_account.save()

        transaction.status = 'completed'
        transaction.save()

        Notification.objects.create(
            user=receiver,
            amount=amount,
            notification_type="Credit Alert"
        )
        Notification.objects.create(
            user=sender,
            amount=amount,
            notification_type="Debit Alert"
        )

        return Response({
            "message": "Transfer completed successfully.",
            "transaction_id": transaction.transaction_id,
            "sender_balance": sender_account.account_balance,
            "receiver_balance": receiver_account.account_balance
        }, status=status.HTTP_200_OK)





class TransferCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number, transaction_id):
        try:
            account = Account.objects.get(account_number=account_number)
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except Account.DoesNotExist:
            return Response({"detail": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in [transaction.sender, transaction.reciever]:
            return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TransactionSerializer(transaction)
        return Response({
            "account": {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "user_id": account.user.id,
                "full_name": getattr(account.user.kyc, "full_name", account.user.username)
            },
            "transaction": serializer.data
        }, status=status.HTTP_200_OK)
