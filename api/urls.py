from django.urls import path,include
from rest_framework import routers
from . import views


router=routers.DefaultRouter()
router.register('Users',views.UserView)
router.register('Coins',views.CoinView)
router.register('Apis',views.ApiKeyView)
router.register('wallets',views.WalletView)
router.register('Registered Transactions',views.RegisteredTransactionsView)
router.register('Fund Request',views.FundRequestView)


urlpatterns = [
    path('',include(router.urls)),
    path('emailtransfer/',views.EmailTransfer.as_view(),name='email_transfer'),
]
