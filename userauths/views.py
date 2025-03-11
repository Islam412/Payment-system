from django.shortcuts import render


from .models import User
from .forms import UserRegisterForm

# Create your views here.


def register(request):
    return render(request,'userauths/sign-up.html')