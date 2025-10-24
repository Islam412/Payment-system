from django.shortcuts import render
from django.views.generic import DetailView


from .models import Home


# Create your views here.


class HomeView(DetailView):
    model = Home
    template_name = 'core/home.html'
    context_object_name = 'home'

    def get_object(self):
        return Home.objects.first()

# def home(request):
#     return render(request, 'core/home.html')