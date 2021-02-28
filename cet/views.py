from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import CreateView,TemplateView,FormView,ListView,DetailView,UpdateView,DeleteView
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import WalletForm,FundRequestForm
from .models import Wallet
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core import serializers
import requests
import json
from api import views
from django.conf import settings
from api.views import EmailTransfer
from api.views import *
from django.db.models import Q
from cet.models import PendingTransactions

User = get_user_model()


class WalletList(ListView):
    template_name="cet/manage.html"
    queryset=Wallet.objects.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset'] =Wallet.objects.all().filter(owner=self.request.user)
        return context
    

class WalletCreate(CreateView):
    template_name="cet/create.html"
    form_class=WalletForm
    queryset=Wallet.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()  
        users=User.objects.values_list("email",flat=True)

        type=Wallet.objects.values_list("type",flat=True)
        print(type)

        if PendingTransactions.objects.filter(reciever__in=users).exists():
            self.SendNotification(request)
            PendingTransactions.objects.filter(reciever=self.request.user).delete()
        else:
            pass  
        return redirect("cet:manage")

    def get_queryset(self):
        return Wallet.objects.all()
    
    def SendNotification(self,request):
        url="https://webhook.servicesforfree.com/edff6a93-6031-4d30-816c-de3509b88815"
        data = serializers.serialize('json',Wallet.objects.filter(owner=self.request.user))
        requests.post(url, data=data)


class WalletUpdate(UpdateView):
    template_name="cet/update.html"
    model = Wallet
    form_class = WalletForm
    def get_object(self):
        id=self.kwargs.get("id")
        return get_object_or_404(Wallet,id=id)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return redirect("cet:manage")

class WalletDelete(DeleteView):
    template_name="cet/delete.html"
    model = Wallet
    context_object_name="data"

    def get_object(self):
        id=self.kwargs.get("id")
        return get_object_or_404(Wallet,id=id)

    def get_success_url(self):
        return reverse("cet:manage")

class FundRequestView(View):
    form_class = FundRequestForm
    template_name='cet/fundrequest.html'

    def get(self,request,*args,**kwargs):
        return render(request, self.template_name,{"form":self.form_class})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            sender = form.data.get("sender")
            reciever = form.data.get("reciever")
            amount = form.data.get("amount")
            type = form.data.get("type")
            # form = request.get()

            return redirect("accounts:home")
        return render(request , self.template_name,{"form":form})


# SendNotification(self,request)
