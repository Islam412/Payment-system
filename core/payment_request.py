from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from decimal import Decimal


from core.models import Transaction
from account.models import Account



@login_required
def search_users_request(request):
    account = Account.objects.all() ## all the account in my db
    query = request.POST.get("account_number") ## <input name="account_number">

    if query:
        account = account.filter(
            Q(account_number=query)|
            Q(account_id=query)

        ).distinct()
    
    context = {
        "account": account,
        "query": query,
    }
    return render(request, "payment_request/search-users.html", context)


def amount_request(request , account_number):
    account = Account.objects.get(account_number=account_number)

    context = {
        "account": account,
    }
    return render(request, "payment_request/amount-request.html", context)