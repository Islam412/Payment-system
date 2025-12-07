from django.urls import path

from account import views
from .api import AccountDetailAPI, KYCSubmitAPI


app_name = 'account'


urlpatterns = [
    path('kyc/', views.kyc_registration, name='kyc-registration'),
    path('', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #api
    path("api/account/", AccountDetailAPI.as_view(), name="api-account-detail"),
    path("api/kyc/", KYCSubmitAPI.as_view(), name="api-kyc-submit"),
]
