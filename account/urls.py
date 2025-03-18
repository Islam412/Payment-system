from django.urls import path

from account import views


app_name = 'account'


urlpatterns = [
    path('kyc/', views.kyc_registration, name='kyc-registration'),
    path('', views.account, name='account'),
]
