from django.shortcuts import render , redirect
from django.views.generic import DetailView


from .models import Home


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
