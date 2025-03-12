from django.urls import path

from userauths import views


app_name = 'core'


urlpatterns = [
    path('', views.home, name='home'),
]