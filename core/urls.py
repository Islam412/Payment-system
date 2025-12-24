from django.urls import path

from core import views , transfer , transaction , payment_request , credit_card 
from .views import HomeView , contatct_us , need_help , about_us , create_notification
from .api import CreditCardDetailAPIView , FundCreditCardAPIView , WithdrawCreditCardAPIView , DeleteCreditCardAPIView , SearchUsersRequestAPIView , AmountRequestAPIView , AmountRequestProcessAPIView , AmountRequestConfirmationAPIView , AmountRequestFinalProcessAPIView , AmountRequestCompletedAPIView , SettlementConfirmationAPIView , SettlementProcessingAPIView , SettlementCompletedAPIView , DeletePaymentRequestAPIView

app_name = 'core'


urlpatterns = [
    #core
    path('', HomeView.as_view(), name='home'),
    path('contatct',contatct_us, name='contatct_us'),
    path('faq',need_help, name='faq'),
    path('about-us',about_us, name='about_us'),
    path('create-notification/', create_notification, name='create_notification'),

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
    path('amount-request-final-process/<account_number>/<transaction_id>/', payment_request.amount_request_final_process, name='amount-request-final-process'),
    path('amount-request-completed/<account_number>/<transaction_id>/', payment_request.request_completed, name='amount-request-completed'),

    # request Settled
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.settlement_completed, name="settlement-completed"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.delete_payment_request, name="delete-request"),

    # credit card
    path('card/<card_id>/', credit_card.card_detail, name='card-detail'),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete_card"),

    # api credite card
    path("api/credit-cards/<str:card_id>/", CreditCardDetailAPIView.as_view(), name="credit-card-detail-api"),
    path("api/credit-cards/fund/<str:card_id>/", FundCreditCardAPIView.as_view(), name="fund-credit-card-api"),
    path("api/credit-cards/withdraw/<str:card_id>/", WithdrawCreditCardAPIView.as_view(), name="withdraw-credit-card-api"),
    path("api/credit-cards/delete/<str:card_id>/", DeleteCreditCardAPIView.as_view(), name="delete-credit-card-api"),

    # payment requist
    path("api/search-users/", SearchUsersRequestAPIView.as_view(), name="search-users-request-api"),
    path("api/amount-request/<str:account_number>/", AmountRequestAPIView.as_view(), name="amount-request-api"),
    path("api/amount-request/process/<str:account_number>/", AmountRequestProcessAPIView.as_view(), name="amount-request-process-api"),
    path("api/amount-request/confirmation/<str:account_number>/<str:transaction_id>/", AmountRequestConfirmationAPIView.as_view(), name="amount-request-confirmation-api"),
    path("api/amount-request/final/<str:account_number>/<str:transaction_id>/", AmountRequestFinalProcessAPIView.as_view(), name="amount-request-final-api"),
    path("api/amount-request/completed/<str:account_number>/<str:transaction_id>/", AmountRequestCompletedAPIView.as_view(), name="amount-request-completed-api"),
    # >>>>>>>>>>>>>>>Settled API<<<<<<<<<<<<<<<<<<<< #
    path("api/settlement-confirmation/<str:account_number>/<str:transaction_id>/", SettlementConfirmationAPIView.as_view(), name="settlement-confirmation-api"),
    path("api/settlement-process/<str:account_number>/<str:transaction_id>/", SettlementProcessingAPIView.as_view(), name="settlement-process-api"),
    path("api/settlement-completed/<str:account_number>/<str:transaction_id>/", SettlementCompletedAPIView.as_view(), name="settlement-completed-api"),
    path("api/delete-payment-request/<str:account_number>/<str:transaction_id>/", DeletePaymentRequestAPIView.as_view(), name="delete-payment-request-api"),
]