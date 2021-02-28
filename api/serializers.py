from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from cet.models import Wallet,ApiKey,RegisteredTransactions,FundRequest,Coin


class EmailTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('public_key',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url','email','is_dev','owner_wallet','is_active','wallet_counter','api_counter')

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coin
        fields=('id','name')

class ApiKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApiKey
        fields = ('url','api_token','owner','devs','name','is_verified','coin_type','url')

class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Wallet
        fields=('url','owner','public_key','type','auto_deposit')

class RegisteredTransactionsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= RegisteredTransactions
        fields=('url','sender','reciever','type','amount','is_successful')



class FundRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= FundRequest
        fields=('url','sender','reciever','amount','type','security_token','is_successful','is_expired','expiration_date')
# class UnregisteredUserSerializer(serializers.ModelSerializer):
#     email=serializers.EmailField()
    
# class UnregisteredUserSerializer(serializers.ModelSerializer):
#     email=serializers.EmailField()
    

    

# class Hookserializer(serializers.Model
# Serializer):
#     class Meta:
#         model=Wallet
#         fields=("id","owner","type")