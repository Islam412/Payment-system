from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Account , KYC
from.forms import KYCForm
from core.forms import CreditCardForm
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




# def dashboard(request):
#     if request.user.is_authenticated:
#         try:
#             kyc = KYC.objects.get(user=request.user)
#         except:
#             messages.warning(request, "You need to submit your kyc")
#             return redirect("account:kyc-registration")
        
#         account = Account.objects.get(user=request.user)

#         if request.method == "POST":
#             form = CreditCardForm(request.POST)
#             if form.is_valid():
#                 new_form = form.save(commit=False)
#                 new_form.user = request.user
#                 new_form.save()

#                 card_id = new_form.card_id
#                 messages.success(request, "Card Added Successfully.")
#                 return redirect("account:dashboard")
            
#             else:
#                 form = CreditCardForm()

#     else:
#         messages.warning(request, "You need to login to access the dashboard")
#         return redirect("userauths:sign-in")

#     context = {
#         "kyc":kyc,
#         "account":account,
#         "form": form,
#     }
#     return render(request, "account/dashboard.html",context)



def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your KYC")
            return redirect("account:kyc-registration")
        
        account = Account.objects.get(user=request.user)

        # Initialize the form outside of the POST check, so it's always defined
        form = CreditCardForm()  # Ensure form is always defined

        if request.method == "POST":
            form = CreditCardForm(request.POST)  # Reinitialize the form with POST data
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("account:dashboard")
            else:
                # Handle invalid form, but you already initialized it above
                messages.error(request, "Please correct the errors below.")

        context = {
            "kyc": kyc,
            "account": account,
            "form": form,  # Always pass the form to the context
        }
        return render(request, "account/dashboard.html", context)

    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

