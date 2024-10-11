from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPrice(admin.TabularInline):
    model = SubscriptionPrice
    extra = 0
    readonly_fields = ["stripe_price_id", "currency"]
    can_delete = False

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPrice]
    list_display = ['name', 'active']
    readonly_fields = ["stripe_product_id"]



# Register your models here.
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)


#PRICE DEBUG
# class SubscriptionPriceAdmin(admin.ModelAdmin):
#     #inlines = [SubscriptionPrice]
#     list_display = ['interval', 'unit_amount']
#     readonly_fields = ["stripe_price_id"]

# admin.site.register(SubscriptionPrice,SubscriptionPriceAdmin)
