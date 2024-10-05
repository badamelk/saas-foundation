from django.db import models
from django.contrib.auth.models import Group, Permission


SUBSCRIPTIONS_PERMISSIONS = [
            ("advanced", "Advanced Perm"), # subscriptions.advanced
            ("pro", "Pro Perm"), 
            ("basic", "Basic Perm")
        ]

# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, limit_choices_to={"name__icontains" : "Plan"})
    permissions = models.ManyToManyField(Permission, limit_choices_to={"content_type__app_label":"subscriptions", "codename__in": [x[0] for x in SUBSCRIPTIONS_PERMISSIONS]})


    def __str__(self):
        
        return self.name


    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSIONS