from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal, InvalidOperation


from account.models import Account
from core.models import Transaction


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




# def amount_transfer_process(request, account_number):
#     account = Account.objects.get(account_number=account_number) ## Get the account that the money vould be sent to
#     sender = request.user # get the person that is logged in
#     reciever = account.user ##get the of the  person that is going to reciver the money

#     sender_account = request.user.account ## get the currently logged in users account that vould send the money
#     reciever_account = account # get the the person account that vould send the money

#     if request.method == "POST":
#         amount = request.POST.get("amount-send")
#         description = request.POST.get("description")

#         print(amount)
#         print(description)

#         if sender_account.account_balance >= Decimal(amount):
#             new_transaction = Transaction.objects.create(
#                 user=request.user,
#                 amount=amount,
#                 description=description,
#                 reciever=reciever,
#                 sender=sender,
#                 sender_account=sender_account,
#                 reciever_account=reciever_account,
#                 status="processing",
#                 transaction_type="transfer"
#             )
#             new_transaction.save()
            
#             # Get the id of the transaction that vas created nov
#             transaction_id = new_transaction.transaction_id
#             return redirect("core:transfer-confirmation", account.account_number, transaction_id)
#         else:
#             messages.warning(request, "Insufficient Fund.")
#             return redirect("core:amount-transfer", account.account_number)
#     else:
#         messages.warning(request, "Error Occured, Try again later.")
#         return redirect("account:account")



def amount_transfer_process(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        messages.error(request, "Recipient account not found.")
        return redirect("core:search-account")

    user = request.user
    sender = user
    reciever = account.user

    sender_account = user.account
    reciever_account = account

    if request.method == "POST":
        amount = request.POST.get("amount_send")
        description = request.POST.get("description")

        try:
            amount = Decimal(amount)
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect("core:amount-transfer", account.account_number)

        if sender_account.account_balance >= amount and amount > 0:
            new_transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_account=sender_account,
                reciever_account=reciever_account,
                status="processing",
                transaction_type="Transfer"
            )
            return redirect("core:transfer-confirmation", account.account_number, new_transaction.transaction_id)
        else:
            messages.warning(request, "Insufficient funds.")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error occurred. Try again later.")
        return redirect("account:account")




def transfer_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        'account':account,
        'transaction':transaction
    }
    
    return render(request, 'transfer/transfer-confirmation.html', context)
