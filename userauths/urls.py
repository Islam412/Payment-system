from django.urls import path

from userauths import views


urlpatterns = [
    path('sign-up/', views.register, name='sign-up'),
]