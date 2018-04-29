from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url=settings.LOGIN_URI)
def indexMB(request):
    return render(request, "index6.html")