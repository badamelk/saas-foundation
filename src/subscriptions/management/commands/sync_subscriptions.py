from django.core.management.base import BaseCommand
from subscriptions.models import Subscription
from typing import Any

class Command(BaseCommand):
    def handle(self, *args:Any, **options:Any): 
        sub_instance = Subscription.objects.filter(active=True)

        for obj in sub_instance:
            permisions = obj.permissions.all()
            
            for group in obj.groups.all():
                group.permissions.set(permisions)
