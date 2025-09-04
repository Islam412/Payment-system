from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from core.forms import CreditCardForm
from core.models import CreditCard
from account.models import Account



def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request)

    context = {
        "account":account,
        "credit_card":credit_card,
    }

    return redirect(request, 'credit_card/card-detail.html')