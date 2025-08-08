from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from core.models import Transaction
from account.models import Account
from django.contrib import messages



@login_required
def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user).order_by('-id')
    reciever_transaction = Transaction.objects.filter(reciever=request.user).order_by('-id')
    
    context = {
        'sender_transaction':sender_transaction,
        'reciever_transaction':reciever_transaction,
    }
    
    return render(request, 'transaction/transaction-list.html', context)




@login_required
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        'transaction':transaction,
    }
    
    return render(request, 'transaction/transaction-detail.html', context)