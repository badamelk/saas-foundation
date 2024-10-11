# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
from django.conf import settings
from decouple import config

DJANGO_DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
STRIPE_SECRET_KEY= config('STRIPE_SECRET_KEY', cast=str)

if DJANGO_DEBUG:
        stripe.api_key = STRIPE_SECRET_KEY

def stripe_customer_create(raw:bool=False, name:str="", email:str="", metadata:dict={}):

    response = stripe.Customer.create(
        name=name, 
        email=email,
        metadata=metadata
    )

    if raw :
        return response
    return response.id

def stripe_product_create(raw:bool=False, name:str="", metadata={}):
    
    response = stripe.Product.create(name=name, metadata=metadata)

    if raw :
         return response
    return response.id


def stripe_price_create(raw:bool=False, currency="eur",
                        unit_amount=9999,
                        interval="month",
                        product_id=None,
                        metadata={}
                        ):
    
    if product_id is None : 
         return None
    
    response = stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        recurring={"interval": interval},
        product=product_id,
        metadata=metadata
        )
    
    if raw :
         return response
    return response.id

    