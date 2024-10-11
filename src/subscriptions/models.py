from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from helpers import billing



SUBSCRIPTIONS_PERMISSIONS = [
            ("advanced", "Advanced Perm"), # subscriptions.advanced
            ("pro", "Pro Perm"), 
            ("basic", "Basic Perm")
        ]

# Create your models here.
class Subscription(models.Model):
    """
    Subscription ==> Stripe product
    """
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, limit_choices_to={"name__icontains" : "Plan"})
    permissions = models.ManyToManyField(Permission, limit_choices_to={"content_type__app_label":"subscriptions", "codename__in": [x[0] for x in SUBSCRIPTIONS_PERMISSIONS]})
    stripe_product_id = models.CharField(max_length=120, null=True, blank=True)
    order = models.IntegerField(default=-1)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name

    def save(self, *args, **kwargs ):
        if not self.stripe_product_id :
            self.stripe_product_id = billing.stripe_product_create( raw=False, 
                                                            name=self.name,
                                                            metadata={"subscription_id" : self.id}
                                                            )
        return super().save(*args, **kwargs)

    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSIONS
        ordering = ['order', '-updated']



class SubscriptionPrice(models.Model):
    """
    Stripe product price
    """

    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"


    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    stripe_price_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(max_length=120, 
                                default=IntervalChoices.MONTHLY, 
                                choices=IntervalChoices.choices )
    currency = models.CharField(max_length=120, default="eur")
    unit_amount = models.DecimalField(max_digits=10, default=99.99, decimal_places=2)

    @property
    def display_sub_name(self):
        if not self.subscription:
            return "No Plan"
        return self.subscription.name
        

    @property
    def stripe_product_id(self):
        
        if not self.subscription:
            return None
        return self.subscription.stripe_product_id
    
    @property
    def stripe_price(self):
        """"
        remove decimal places for stripe api
        """
        return int(self.unit_amount * 100)


    def __str__(self): 
        return f'{self.unit_amount} {self.currency}'

    def save(self, *args, **kwargs ):
        if not self.stripe_price_id and self.stripe_product_id is not None:
            self.stripe_price_id = billing.stripe_price_create( raw = False,
                                                                currency=self.currency,
                                                                unit_amount=self.stripe_price,
                                                                interval = self.interval,
                                                                product_id=self.stripe_product_id,
                                                                metadata={"subscription_price_id" : self.id}
                                                                )
        return super().save(*args, **kwargs)





class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription} "

def usersubscription_post_save(sender, instance, *args, **kwargs):
    user_subscription_instance = instance
    user = user_subscription_instance.user
    print(user)
    user_subscriptions = user_subscription_instance.subscription
    groups = user_subscriptions.groups.all()
    user.groups.set(groups)

post_save.connect(usersubscription_post_save, sender=UserSubscription)