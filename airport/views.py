from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as login_to_session
from django.contrib.auth.views import logout as djangoLogout
from django.contrib.auth.models import User


def flights_list(request):
    return render(request, 'flight.html')


def flight(request, flightId):
    return HttpResponse("Flight")


@require_POST
def register(request):
    if User.objects.all().filter(username=request.POST['username']).exists():
        registerError = True
    else:
        user = User.objects.create_user(
            username=request.POST['username'], password=request.POST['password'])
        login_to_session(request, user)
    return render(request, 'main.html', locals())


@require_POST
def login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login_to_session(request, user)
    else:
        loginError = True
    return render(request, 'main.html', locals())


def logout(request):
    djangoLogout(request)
    return render(request, 'main.html', locals())

