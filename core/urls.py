from django.urls import path

from core import views
from core import transfer


app_name = 'core'


urlpatterns = [
    path('', views.home, name='home'),

    # transfer
    path('search-account/', transfer.search_users_account_number, name='search-account'),
    path('amount-transfer/<account_number>/', transfer.amount_transfer, name='amount-transfer'),
]