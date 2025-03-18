from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal


from account.models import Account


def search_users_account_number(request):
    return render(request, 'core/search_users_account_number.html')