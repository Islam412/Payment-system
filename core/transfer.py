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
    return render(request, "transfer/amount_transfer.html") 