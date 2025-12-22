from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from account.models import Account
from userauths.models import User
from .models import Home , Notification


# Create your views here.


class HomeView(DetailView):
    model = Home
    template_name = 'core/home.html'
    context_object_name = 'home'

    def get_object(self):
        return Home.objects.first()




def contatct_us(request):
    return render(request,'core/contact.html')


def need_help(request):
    return render(request, 'core/need_help.html')


def about_us(request):
    return render(request, 'core/about-us.html')



@login_required
def create_notification(request):
    receiver_id = request.POST.get('receiver_id')
    amount = request.POST.get('amount')
    notification_type = request.POST.get('notification_type', 'Credit Alert')

    receiver_user = get_object_or_404(User, id=receiver_id)
    sender_account = get_object_or_404(Account, user=request.user)

    notif = Notification.objects.create(
        user=receiver_user,
        sender=sender_account,
        notification_type=notification_type,
        amount=amount
    )

    return JsonResponse({
        "status": "success",
        "sender_name": notif.sender_full_name,
        "sender_image": notif.sender_image_url or "",
        "amount": notif.amount,
        "notification_type": notif.notification_type
    })
