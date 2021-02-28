from django.urls import path
from .views import WalletList,WalletCreate,WalletUpdate,WalletDelete,FundRequestView

app_name = 'cet'



urlpatterns = [
    path('manage/', WalletList.as_view(), name='manage'),
    path('create/', WalletCreate.as_view(), name='create'),
    path('update/<id>/', WalletUpdate.as_view(), name='update'),
    path('delete/<id>/', WalletDelete.as_view(), name='delete'),
    path('fundrequest/', FundRequestView.as_view(),name='fundrequest'),


]


