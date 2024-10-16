from django.urls import path
from .views import deposit, withdraw, balance, payment_history, fund_wallet_manual, transaction_history, transfer, verify_transaction, cancel_transaction, verify_wallet_transfer

urlpatterns = [
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('balance/', balance, name='wallet_balance'),
    path('transactions/', transaction_history, name='transaction_history'),
    path('payments/', payment_history, name='payment_history'),
    path('transfer/', transfer, name='transfer'),
    path('verify/transaction/',
         verify_transaction, name='verify_transaction'),
    path('cancel/transaction/', cancel_transaction, name='cancel_transaction'),
    path('verify/transfer/<int:user_id>/',
         verify_wallet_transfer, name='verify_wallet_transfer'),
]
