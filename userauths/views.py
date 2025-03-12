from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import User
from .forms import UserRegisterForm

# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']

            messages.success(request, f'Account created for {username}! You are now able to log in.')

            new_user = authenticate(
                username = form.cleaned_data['email'],
                password = form.cleaned_data['password1'],
            )

            login(request, new_user)
            return redirect('core:home')
        
    if request.user.is_authenticated:
        messages.success(request, 'You are now logged in')
        return redirect('core:home')

    else:
        # messages.warning(request, "Account created, but automatic login failed. Please log in again.")
        
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request,'userauths/sign-up.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {request.user.username}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password')

    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('core:home')

    else:
        return render(request, 'userauths/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('userauths:sign-in')