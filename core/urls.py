from django.urls import path

from core import views
from core import transfer
from core import transaction


app_name = 'core'


urlpatterns = [
    #core
    path('', views.home, name='home'),

    # transfer
    path('search-account/', transfer.search_users_account_number, name='search-account'),
    path('amount-transfer/<account_number>/', transfer.amount_transfer, name='amount-transfer'),
    path('amount-transfer-process/<account_number>/', transfer.amount_transfer_process, name='amount-transfer-process'),
    path('transfer-confirmation/<account_number>/<transaction_id>/', transfer.transfer_confirmation, name='transfer-confirmation'),
    path('transfer-process/<account_number>/<transaction_id>/', transfer.transfer_process, name='transfer-process'),
    path('transfer-completed/<account_number>/<transaction_id>/', transfer.transfer_completed, name='transfer-completed'),
    
    #transaction
    path('transactions/', transaction.transaction_lists, name='transactions'),
    path('transactions-detail/', transaction.transaction_detail, name='transactions-detail'),
]