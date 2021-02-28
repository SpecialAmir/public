from decimal import Context
from django.contrib.auth.forms import UserCreationForm
from django.http import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.generic import TemplateView,FormView
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .forms import CustomUserCreationForm, LoginForm,SignupView2
from django.urls import reverse_lazy
from django.contrib import messages
from cet.models import ApiKey
from .utils import generate_token
from django.utils.http import urlsafe_base64_encode
from cet.models import PendingTransactions


User = get_user_model()



# @login_required(login_url="login")
class IndexView(TemplateView):

    template_name = 'index.html'
    def get_context_data(self,*args,**kwargs):
        self.context = super().get_context_data(*args,**kwargs)

        self.context['segment'] = 'index'

        return self.context




class SignupView(View):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/register.html'

    def get(self,request,*args,**kwargs):        
        return render(request, self.template_name,{"form":self.form_class})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.data.get("email")
            password = form.data.get("password")
            user = User.objects.create_user(email,password)
            return redirect("accounts:login")
        return render(request , self.template_name,{"form":form})


class SignupView2(View):
    template_name = 'invitation/signup2.html'
    form_class= SignupView2
    def get(self,request,token):
        transaction=get_object_or_404(PendingTransactions,token=token)
        return render(request,self.template_name,{"email":transaction.reciever,"form":self.form_class})   

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            transaction=get_object_or_404(PendingTransactions,token=token)
            email=transaction.reciever
            password = form.data.get("password")
            user = User.objects.create_user(email,password,is_active=True)
            user.save()
            return redirect("accounts:login")
   



class LoginView(FormView):
    model=User
    form_class=LoginForm
    template_name='accounts/login.html'

    def get(self,request,*args,**kwargs):
        
        return render(request, self.template_name,{"form":self.form_class})

    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        user= authenticate(request,email=email,password=password)
        if user is not None:
            print(request.POST)
            login(request,user)
            if 'next' in request.GET:
                return redirect(request.POST.get('next'))
            return redirect('accounts:home')
            
class ActivateAccount(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO,'account activated successfuly')
            return redirect("accounts:login")
        return render (request,'email/activation-failed.html',status=401)



class LogoutView(View):   
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')




