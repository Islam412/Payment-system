from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from decimal import Decimal

from core.models import CreditCard
from account.models import Account



def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account":account,
        "credit_card":credit_card,
    }

    return render(request, 'credit_card/card-detail.html', context)



def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account

    if request.method == "POST":
        amount = request.POST.get("funding_amount")

        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()

            credit_card.amount += Decimal(amount)
            credit_card.save()

            messages.success(request, "Funding Successful")
            return redirect('core:card-detail',credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)


