from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from  visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings



LOGIN_URL = settings.LOGIN_URL
# Create your views here.

def homepage(request):
    return default_view(request)

def default_view(request):
    currentPage = "homepage"
    PageVisit.objects.create(path=request.path)
    qs_page = PageVisit.objects.filter(path=request.path)
    qs_all = PageVisit.objects.all()
    
    user = { 
        'username' : "",
        'currentPage' : currentPage,
        'pageVisits' : qs_page.count(),
        'siteVisits' : qs_all.count()
    }

    return render(request, "home.html", user )


@login_required(login_url=LOGIN_URL)
def user_only_view(request):
    current_user = request.user
    context = {
        "user" : current_user
    }

    return render(request, "protected/logged_user_page.html", context)

@staff_member_required
def staff_only_view(request):
    current_user = request.user
    context = {
        "user" : current_user
    }

    return render(request, "protected/staff_user_page.html", context)