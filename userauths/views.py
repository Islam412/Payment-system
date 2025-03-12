from django.shortcuts import render


from .models import User
from .forms import UserRegisterForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request,'userauths/sign-up.html', context)