from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from django.db.models import Q
from django.core.mail import send_mail
from .serializers import UserSerializer ,CoinSerializer,ApiKeySerializer,WalletSerializer,RegisteredTransactionsSerializers,FundRequestSerializer,EmailTransferSerializer
from cet.models import Coin,ApiKey,Wallet,RegisteredTransactions,FundRequest
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout,get_user_model
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements
from rest_framework.views import APIView
from main import settings
from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core import serializers
import requests
import json
from cet.models import RegisteredTransactions , PendingTransactions
from .utils import random_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
User=get_user_model()
class UserView(ProtectedResourceView,viewsets.ModelViewSet):
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {}
    queryset = get_user_model().objects.all()
    serializer_class=UserSerializer


class CoinView(ProtectedResourceView,viewsets.ModelViewSet):
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {}
    queryset = Coin.objects.all()
    serializer_class=CoinSerializer


class ApiKeyView(ProtectedResourceView,viewsets.ModelViewSet):
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {}
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer


class WalletView(ProtectedResourceView,viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
    "GET": [["read"]],
}


class RegisteredTransactionsView(ProtectedResourceView,viewsets.ModelViewSet):
    queryset = RegisteredTransactions.objects.all()
    serializer_class = RegisteredTransactionsSerializers


class FundRequestView(ProtectedResourceView,viewsets.ModelViewSet):
    queryset = FundRequest.objects.all()
    serializer_class = FundRequestSerializer


class EmailTransfer(APIView):
    def get_queryset(self):
        return Wallet.objects.all()

    # def send_email(self,request):
    def send_email(self,instance):
        current_site=settings.DEFAULT_DOMAIN
        subject="Invitation to register"
        message = render_to_string('invitation/invitation.html', {
        'domain': current_site,
        'token': str(instance.token)})
        send_mail(subject, message,settings.EMAIL_HOST_USER,[self.email],fail_silently=False)

    def post(self,request,*args,**kwargs):
        self.email=request.data['email']
        self.type=request.data['type'] 
        self.amount=request.data['amount']
        valid_key = self.get_queryset().filter(Q(owner__email__iexact=self.email),Q(type__name__icontains=self.type),Q(auto_deposit=True)).distinct()
        if valid_key:
            serializer = EmailTransferSerializer(valid_key,many=True)
            return Response(serializer.data)
        else:
            transaction= PendingTransactions.objects.create(sender=self.request.user,reciever=self.email,
            type=self.type,amount=self.amount)
            transaction.save()
            # self.send_email(request)
            self.send_email(transaction)
            return Response("we sent an email")
                

