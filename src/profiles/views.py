from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
@login_required
def profile_view(request, username=None, *args, **kwargs):
    user = request.user
    user_if_exist = get_object_or_404(User, username=username)

    return render(request, 'user.html')

