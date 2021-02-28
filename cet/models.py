from django.db import models
from cet.choices import COIN_CHOICES
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
import uuid



class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True,blank=True)

    class Meta:
        abstract = True


class Coin(BaseModel):
    name=models.CharField(max_length=15,choices=COIN_CHOICES)

    def __str__(self):
        return self.name


class ApiKey(BaseModel):
    api_token=models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(),related_name='owner_apikeys',on_delete=models.CASCADE)
    devs = models.ManyToManyField(get_user_model())
    name=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    coin_type=models.ManyToManyField(Coin)
    url=models.URLField(max_length=200,blank=True,default=None)

    def __str__(self):
        return str(self.owner)

    # @receiver(post_save, sender=refrencing an admin user)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)





class Wallet(BaseModel):
    name=models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(),related_name='owner_wallet',on_delete=models.CASCADE)
    public_key=models.CharField(max_length=451)
    type= models.ForeignKey(Coin,on_delete=models.DO_NOTHING)
    auto_deposit=models.BooleanField(default=True)

    def __str__(self):
        return str(self.owner)

    




    # def type_checker(type):
    #     pass

class RegisteredTransactions(BaseModel):
    sender=models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING)
    reciever=models.EmailField()
    type=models.CharField(max_length=200)
    amount=models.DecimalField(max_digits=18,decimal_places=8)
    is_successful=models.BooleanField(default=False)

class PendingTransactions(BaseModel):
    sender=models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING)
    reciever=models.EmailField()
    type=models.CharField(max_length=200)
    amount=models.DecimalField(max_digits=18,decimal_places=8)
    is_successful=models.BooleanField(default=False)
    token=models.UUIDField(default=uuid.uuid4,editable=False)
    


class FundRequest(BaseModel):
    sender=models.EmailField(max_length=200)
    reciever=models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING)
    amount=models.DecimalField(max_digits=18,decimal_places=8)
    type=models.OneToOneField(Coin,on_delete=models.DO_NOTHING)
    security_token=models.CharField(max_length=15)
    is_successful=models.BooleanField(default=False)
    is_expired=models.BooleanField(default=False)
    expiration_date=models.DateTimeField()