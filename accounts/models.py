from django.db import models
from cet.models import BaseModel
from django.core.mail import send_mail
from main import settings
from django.template.loader import render_to_string
from .utils import generate_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import AbstractUser,BaseUserManager
from cet import models as cm
# from api.views import send_email
# from api.utils import random_token

class AccountManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        # extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        if user.is_active == False:
            current_site = settings.DEFAULT_DOMAIN
            subject = 'Activate Your Crypto Email Transfer Account'
            message = render_to_string('email/activation-email.html', {'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),})
            user.email_user(subject, message,settings.EMAIL_HOST_USER)
        
        return user


    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_dev', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

# user app
class User(AbstractUser,BaseModel):
    email = models.EmailField(verbose_name='email',max_length=100,unique=True)
    username = None
    last_login = models.DateTimeField(verbose_name='last login',auto_now_add=True)
    is_dev = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # groups = models.ManyToManyField()


    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    objects= AccountManager()

    def __str__(self):
        return self.email

    @property
    def api_counter(self):
        return cm.ApiKey.objects.filter(owner=self).count()
    
    @property
    def wallet_counter(self):
        return cm.Wallet.objects.filter(owner=self).count()
    
    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)
