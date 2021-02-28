from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
User = get_user_model()









class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control",
                "id":"myInput"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))

    class Meta(UserCreationForm):
        model = User
        fields = ('email','password')



class LoginForm(AuthenticationForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control",
                "id":"myInput"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))


    class Meta:
        model=User
        fields=('email','password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class SignupView2(UserCreationForm):
    password2=None
    username=None
    class Meta:
        model=User
        fields=('password',)


class SignupForm(UserCreationForm):
    password2=None
    username=None
    class Meta:
        model=User
        fields=('email','password')




