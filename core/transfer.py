from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal


from account.models import Account


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
    account = Account.objects.get(account_number=account_number) # Get the account that the money vould## Get the account that the be sent to
    user = request.user # get the person that is logged in
    reciever = account.user ##get the of the  person that is going to reciv
    
    sender_account = request.user.account ## get the currently logged in users account that vould send the money
    reciever_account = account # get the the person account that vould send the money