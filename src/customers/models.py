from django.db import models
#from django.contrib.auth import get_user_model
from django.conf import settings
from helpers import billing
# Allauth signals
from allauth.account.signals import (user_signed_up as allauth_sign_up_signal, 
                                     email_confirmed as allauth_email_confirmed_signal,
                                     )
from allauth.socialaccount.signals import (pre_social_login as allauth_pre_social_login_signal,
                                           social_account_added as allauth_social_account_added_signal)
from allauth.utils import get_user_model
from allauth.account.utils import has_verified_email


user = settings.AUTH_USER_MODEL
User = get_user_model()
social_account_signup_data = {}

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    init_email= models.EmailField(null=True, blank=True)
    init_email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs ):
        if not self.stripe_id :
            if self.init_email and self.init_email_confirmed : 
                self.stripe_id = billing.stripe_customer_create(raw=False, 
                                                            name=self.user.username, 
                                                            email=self.user.email,
                                                            metadata={'user_id':self.user.id})
            return super().save(*args, **kwargs)
        

def allauth_sign_up_signal_handler(request, user, *args, **kwargs):
    print('THROUGH NORMAL SIGN UP')
    
    Customer.objects.create(
        user = user,
        init_email = user.email,
        init_email_confirmed = False
    )

    #if user email has been verified automatically through social account connection 
    if has_verified_email(user, email=user.email) : 
        update_customer_model(Customer, email=user.email)

allauth_sign_up_signal.connect(allauth_sign_up_signal_handler)


def allauth_email_confirmed_signal_handler(request, email_address, *args, **kwargs):
    print('EMAIL CONFIRMED HANDLER')
    update_customer_model(Customer, email=email_address)

allauth_email_confirmed_signal.connect(allauth_email_confirmed_signal_handler)


def update_customer_model(instance, email):
    qs = instance.objects.filter(
        init_email=email,
        init_email_confirmed=False,
        )
    for obj in qs:
        obj.init_email_confirmed = True
        obj.save()