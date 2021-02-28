from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Wallet,Coin,FundRequest
from .choices import COIN_CHOICES
User = get_user_model()



class WalletForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder" : "name",                
                "class": "form-control"
            }
        ))
    type = forms.ModelChoiceField(queryset=Coin.objects.all(),widget=forms.Select(
            attrs={               
                "class": "form-control",
                
            }
        ))
    public_key = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder" : "Public Key",                
                "class": "form-control"
            }
        ))
    # CHOICES=[('Enable','Enable'),
    #      ('Disable','Disable')]
    # Status=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(
    #     attrs={
           
    #          "class":"form-radio-input"
    #     }
    # ))
    
    class Meta:
        model=Wallet
        fields=('name','type','public_key','auto_deposit',)
 
class FundRequestForm(forms.ModelForm):
    
    sender = forms.EmailField(widget=forms.TextInput(
            attrs={
                "placeholder" : "sender",                
                "class": "form-control"
            }
        ))
    type = forms.ModelChoiceField(queryset=Coin.objects.all(),widget=forms.Select(
            attrs={               
                "class": "form-control",
                
            }
        ))
    amount = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder" : "amount",                
                "class": "form-control"
            }
        ))
        
    class Meta:
        model= FundRequest
        fields=('sender',  'amount', 'type',)


