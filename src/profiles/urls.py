
from django.urls import path, include
from .views import profile_view

urlpatterns = [
    path('<username>/', profile_view, name='profile')
]
