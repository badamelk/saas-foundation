from django.shortcuts import render
from  visits.models import PageVisit

# Create your views here.

def homepage(request):
    return default_view(request)

def default_view(request):
    currentPage = "homepage"
    PageVisit.objects.create(path=request.path)
    qs_page = PageVisit.objects.filter(path=request.path)
    qs_all = PageVisit.objects.all()
    
    user = { 
        'username' : "Kibam",
        'currentPage' : currentPage,
        'pageVisits' : qs_page.count(),
        'siteVisits' : qs_all.count()
    }

    return render(request, "home.html", user )

