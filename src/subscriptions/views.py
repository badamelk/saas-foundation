from django.shortcuts import render
from django.urls import reverse
from .models import SubscriptionPrice

# Create your views here.
def subscription_price_view(request, interval="month"):
    qs_monthly = SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervalChoices.MONTHLY)
    qs_yearly = SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervalChoices.YEARLY)
    interval_yearly = SubscriptionPrice.IntervalChoices.YEARLY

    qs_interval = qs_monthly
    if interval == interval_yearly:
        qs_interval = qs_yearly

    url_path_name = "pricing_toggle"
    month_url = reverse(url_path_name, kwargs={"interval":"month"})
    year_url = reverse(url_path_name, kwargs={"interval":"year"})

    context = {"qs_interval" : qs_interval,
               "month_url" : month_url,
               "year_url" : year_url,
                "interval" : interval }

    return render(request, 'subscription/pricing.html', context)