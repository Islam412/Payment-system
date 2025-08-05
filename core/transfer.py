from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal, InvalidOperation


import account
from account.models import Account
from core.models import Transaction
from userauths.models import User

@login_required
def search_users_account_number(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()

    context = {
        "account": account,
        "query": query,
    }
    return render(request, 'core/search-user-by-account-number.html',context)




def amount_transfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "Account dosen't exist")
        return redirect("core:search-account")
    
    context = {
        "account": account,
    }
    return render(request, "transfer/amount_transfer.html", context) 




def amount_transfer_process(request, account_number):
    account = get_object_or_404(Account, account_number=account_number)  # Get the receiver's account
    sender = request.user  # Logged-in user
    receiver = account.user  # Receiver user

    sender_account = sender.account  # Sender's account
    receiver_account = account  # Receiver's account

    if request.method == "POST":
        amount = request.POST.get("amount_send")
        description = request.POST.get("description")

        try:
            amount = Decimal(amount)
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect("core:amount-transfer", account.account_number)

        if sender_account.account_balance >= amount:
            new_transaction = Transaction.objects.create(
                user=sender,
                amount=amount,
                description=description,
                reciever=receiver,
                sender=sender,
                sender_account=sender_account,
                reciever_account=receiver_account,
                status="processing",
                transaction_type="transfer"
            )
            
            return redirect("core:transfer-confirmation", account.account_number, new_transaction.transaction_id)
        else:
            messages.warning(request, "Insufficient funds.")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error occurred. Try again later.")
        return redirect("account:account")




# def amount_transfer_process(request, account_number):
#     try:
#         account = Account.objects.get(account_number=account_number)
#     except Account.DoesNotExist:
#         messages.error(request, "Recipient account not found.")
#         return redirect("core:search-account")

#     user = request.user
#     sender = user
#     reciever = account.user

#     sender_account = user.account
#     reciever_account = account

#     if request.method == "POST":
#         amount = request.POST.get("amount_send")
#         description = request.POST.get("description")

#         try:
#             amount = Decimal(amount)
#         except (InvalidOperation, TypeError):
#             messages.error(request, "Invalid amount entered.")
#             return redirect("core:amount-transfer", account.account_number)

#         if sender_account.account_balance >= amount and amount > 0:
#             new_transaction = Transaction.objects.create(
#                 user=user,
#                 amount=amount,
#                 description=description,
#                 reciever=reciever,
#                 sender=sender,
#                 sender_account=sender_account,
#                 reciever_account=reciever_account,
#                 status="processing",
#                 transaction_type="Transfer"
#             )
#             return redirect("core:transfer-confirmation", account.account_number, new_transaction.transaction_id)
#         else:
#             messages.warning(request, "Insufficient funds.")
#             return redirect("core:amount-transfer", account.account_number)
#     else:
#         messages.warning(request, "Error occurred. Try again later.")
#         return redirect("account:account")




def transfer_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist.")
        return redirect("account:account")
    
    context = {
        'account':account,
        'transaction':transaction
    }
    
    return render(request, 'transfer/transfer-confirmation.html', context)



def transfer_process(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user  # Logged-in user
    receiver = account.user  # Receiver user

    sender_account = sender.account  # Sender's account
    receiver_account = account  # Receiver's account

    completed = False

    if request.method == 'POST':
        pin_number = request.POST.get("pin-number")

        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = 'completed'
            transaction.save()

            # Deduct the amount from sender's balance
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # Add the amount to receiver's balance
            receiver_account.account_balance += transaction.amount
            receiver_account.save()

            messages.success(request, "Transfer Successful.")
            return redirect('account:account')
        else:
            messages.warning(request, "Incorrect Pin.")
            return redirect('core:transfer-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occured, Try again later.")
        return redirect('account:account')




def transfer_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("account:account")
    context = {
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer-completed.html", context)