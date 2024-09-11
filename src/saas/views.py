from django.shortcuts import render
from  visits.models import PageVisit

# Create your views here.

def default_view(request):
    return homepage(request)

def homepage(request):
    currentPage = homepage.__name__
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

