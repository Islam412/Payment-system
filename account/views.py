from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Account , KYC
from.forms import KYCForm
from core.forms import CreditCardForm
from core.models import CreditCard
# Create your views here.


@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submitted successfully, In review now.")
            return redirect("core:home")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "account/kyc-form.html", context)



@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-registration")
        
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "account/account.html", context)





def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-registration")
                
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")

        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("account:dashboard")
        else:
            form = CreditCardForm()

    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
        "form":form,
        "credit_card":credit_card,
    }
    return render(request, "account/dashboard.html", context)
    
    

class DeleteAccountView(LoginRequiredMixin, View):

    def get(self, request):
        cards = CreditCard.objects.filter(user=request.user)

        return render(request, "account/delete_account_confirm.html", {
            "cards": cards
        })

    def post(self, request):
        user = request.user
        
        account = Account.objects.get(user=user)
        balance = account.account_balance  

        card_id = request.POST.get("card_id")

        try:
            card = CreditCard.objects.get(id=card_id, user=user)
        except:
            messages.error(request, "Invalid card selection.")
            return redirect("account:delete-account")

        card.balance += balance
        card.save()

        messages.info(
            request, 
            f"Your balance of {balance} has been transferred to your selected card ending with {card.card_id}."
        )

        user.delete()

        messages.success(request, "Your account has been deleted successfully.")
        return redirect("core:home")
