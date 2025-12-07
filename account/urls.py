from django.urls import path

from account import views
from . import api

app_name = 'account'


urlpatterns = [
    path('kyc/', views.kyc_registration, name='kyc-registration'),
    path('', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #api
    path("api/account/", api.account_api),
    path("api/kyc/", api.kyc_api),
    path("api/dashboard/", api.dashboard_api),
]
