from django.urls import path

from account import views
from . import api

app_name = 'account'


urlpatterns = [
    path('kyc/', views.kyc_registration, name='kyc-registration'),
    path('', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #api
    path("api/account/", api.account_api, name="account_api"),
    path("api/kyc/", api.kyc_api , name='kyc_api'),
    path("api/dashboard/", api.dashboard_api, name="dashboard_api"),

    # api based view
    path("api/generic/account/", api.AccountViewAPI.as_view(), name="account-api"),
    path("api/generic/kyc/", api.KYCViewAPI.as_view(), name="kyc-api"),
    path("api/generic/dashboard/", api.DashboardViewAPI.as_view(), name="dashboard-api"),
    path("api/generic/add-card/", api.AddCardViewAPI.as_view(), name="add-card-api"),
]


