from django.urls import path

from core import views , transfer , transaction , payment_request


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
    
    # transaction
    path('transactions/', transaction.transaction_lists, name='transactions'),
    path('transactions-detail/<transaction_id>/', transaction.transaction_detail, name='transaction-detail'),
    
    # payment request
    path('request-search-account/', payment_request.search_users_request, name='request-search-account'),
    path('amount-request/<account_number>/', payment_request.amount_request, name='amount-request'),
    path('amount-request-process/<account_number>/', payment_request.amount_request_process, name='amount-request-process'),
    path('amount-request-confirmation/<account_number>/<transaction_id>/', payment_request.amount_request_confirmation, name='amount-request-confirmation'),
]