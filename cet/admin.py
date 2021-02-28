from django.contrib import admin
from cet.models import (
    Coin,
    ApiKey,
    Wallet,
    RegisteredTransactions,
    PendingTransactions,
    FundRequest,
    )


class WalletAdmin(admin.ModelAdmin):
    list_display = ('name','owner','type','created_at','auto_deposit')
    search_fields = ('owner__email',)
    list_filter=('type',)
    ordering=()
    fieldsets=()




class ApiAdmin(admin.ModelAdmin):
    list_display = ('owner','developers','name','coin_types','is_verified','url','created_at')
    search_fields = ('owner__email','devs__email')
    ordering=()
    filter_horizontal=('devs','coin_type')
    list_filter=('coin_type','is_verified','devs')
    fieldsets=()

    def developers(self, obj):
        return ", ".join([str(p) for p in obj.devs.all()])
    def coin_types(self, obj):
        return ", ".join([str(p) for p in obj.coin_type.all()])


class PendingTransactionsAdmin(admin.ModelAdmin):
    list_display = ('sender','reciever','type','amount','created_at','is_successful')
    search_fields = ('sender__email','reciever__owner')
    list_filter=('type','is_successful',)

class RegisterTransactionAdmin(admin.ModelAdmin):
    list_display = ('sender','reciever','type','amount','created_at','is_successful')
    search_fields = ('sender__email','reciever__owner')
    list_filter=('type','is_successful',)

class FundRequestAdmin(admin.ModelAdmin):
    list_display = ('sender','reciever','type','amount','created_at','expiration_date','is_successful','is_expired',)
    search_fields = ('sender__email','reciever__owner','security_token','is_expired','expiration_date')
    list_filter=('type','is_successful',)





admin.site.register(Coin)
admin.site.register(ApiKey,ApiAdmin)
admin.site.register(Wallet,WalletAdmin)
admin.site.register(RegisteredTransactions,RegisterTransactionAdmin)
admin.site.register(PendingTransactions,PendingTransactionsAdmin)
admin.site.register(FundRequest,FundRequestAdmin)