from django.shortcuts import render

# Create your views here.

def homepage(request):
    user = { 
        'name' : "Kibam"
    }
    return render(request, "home.html", user )
