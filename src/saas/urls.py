"""
URL configuration for saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    
    path('', views.default_view, name='home'),
    path('home/', views.homepage),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
    path('protected/user_page/', views.user_only_view),
    path('staff_page/', views.staff_only_view),
    path('none', RedirectView.as_view(url='/admin'), name='staff'),
    path('admin/', admin.site.urls ),
    
]
